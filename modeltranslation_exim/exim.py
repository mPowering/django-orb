# -*- coding: utf-8 -*-

import importlib
import sys
from collections import defaultdict

import polib
from django.apps import apps


class DatabaseTranslations(object):
    """
    Data interface for extracting values from model fields and exporting to a
    .po file for out-of-application translation.

    >>> to_translate = {myapp.Resource: ['title', 'summary'], myapp.Site: ['name']}
    >>> exporter = DatabaseTranslations(to_translate)
    >>> with open("somefile.po", "w") as po_file:
    >>>     exporter.save(po_file)

    The data is stored in a dictionary of base strings (msgid) as keys and
    translated values (msgstr) and occurrences.::

        {
            u"Hello": {
                "msgstr": "Holá",
                "occurrences": [
                    ("myapp.SomeModel.field_name", 12),
                    ("myapp.SomeModel.field_name", 27),
                ],
            },
        }

    It might be better stored as a graph to allow for a consistent interface
    for both export and import.

    """

    def __init__(self, model_fields, language=None):
        """
        Initialize the instance.

        Args:
            model_fields: a dictionary of model Classes and field names
            language: optional language code for retrieving existing translations

        """
        self.models_and_fields = model_fields
        self.strings = defaultdict(lambda: {"msgstr": u"", "occurrences": []})
        self.target_language = language
        self.po = polib.POFile()
        self.po.metadata = self._meta()

        if not self.target_language:
            self._untranslated()
        else:
            self._translated()

        for entry in self.get_entries():
            self.po.append(entry)

    @classmethod
    def from_paths(cls, *args):
        """
        Creates a new DatabaseTranslations instance from a sequence of
        module.Class.field_name paths.

        Args:
            *args: combined module, class, field name dotted paths

        Returns:
            a new DatabaseTranslations instance

        """
        class_and_field = defaultdict(list)
        for dotted_path in args:
            module_name, class_name, field_name = dotted_path.rsplit(".", 2)

            module = importlib.import_module(module_name)

            try:
                model_class = getattr(module, class_name)
            except AttributeError:
                model_class = apps.get_model(module_name, class_name)

            class_and_field[model_class].append(field_name)

        return DatabaseTranslations(class_and_field)

    def _untranslated(self):
        """
        Makes no attempt to return existing translations

        Returns:

        """
        for model_class in self.models_and_fields.keys():
            class_path = ".".join([model_class.__module__, model_class.__name__])
            for instance in model_class._default_manager.all():
                for field_name in self.models_and_fields[model_class]:
                    try:
                        field_value = polib.escape(getattr(instance, field_name))
                    except AttributeError:
                        continue
                    if not field_value:
                        continue
                    self.strings[field_value]['occurrences'].append(
                        (".".join([class_path, field_name]), instance.pk))

    def _translated(self):
        """

        Returns:

        """
        from modeltranslation.utils import build_localized_fieldname
        for model_class in self.models_and_fields.keys():
            class_path = ".".join([model_class.__module__, model_class.__name__])
            for instance in model_class._default_manager.all():
                for field_name in self.models_and_fields[model_class]:
                    field_value = getattr(instance, field_name)
                    msgstr = getattr(instance, build_localized_fieldname(field_name, self.target_language))
                    self.strings[field_value]['msgstr'] = msgstr
                    self.strings[field_value]['occurrences'].append(
                        (".".join([class_path, field_name]), instance.pk))

    def _meta(self, **kwargs):
        """
        Builds the _meta info
        """
        defaults = {
            "Project-Id-Version": "PACKAGE VERSION",
            "Report-Msgid-Bugs-To": "",
            "POT-Creation-Date": "2014-01-21 00:57+0100",
            "PO-Revision-Date": "YEAR-MO-DA HO:MI+ZONE",
            "Last-Translator": "FULL NAME <EMAIL@ADDRESS>",
            "Language-Team": "LANGUAGE <LL@li.org>",
            "Language": "",
            "MIME-Version": "1.0",
            "Content-Type": "text/plain; charset=UTF-8",
            "Content-Transfer-Encoding": "8bit",
        }
        defaults.update(**kwargs)
        return defaults

    def save(self, out=sys.stdout):
        """
        Writes the po file contents to sys.stdout or file stream
        """
        out.write(self.po.__unicode__().encode('utf-8'))

    def get_entries(self):
        for msgid, data in self.strings.items():
            yield polib.POEntry(msgid=msgid, msgstr=data['msgstr'], occurrences=data['occurrences'])


class POTranslations(object):
    """
    Interface for importing from a PO file into database.

    There are two basic ways to update database records with this content:

    1. Updating each object (database row) one by one
    2. Updating tables for each field/string combination

    The second should be quicker if strings are frequently used across
    multiple rows in the same table. The first should be quicker if
    objects (rows) have multiple fields to update.

    The data structure is optimized for the first strategy::

        {
            SomeClass: {
                12: {
                    'title': 'New translated string',
                    'description': 'New translated string',
                }
            }
        }

    It will make one update per object (whether this is one `update`
    or one pair of `get`/`save`).

    Ideally - barring a flag to 'safely' save the data - the structure
    could be reoptimized depending on what it looks like after loading,
    or at the least an alternate save strategy could be used.

    """
    def __init__(self, pofile_name, language, output=None):
        """
        Args:
            pofile_name: path to the file
            language: the language to output to
        """
        self.po = polib.pofile(pofile_name)
        self.language = language
        self.output = output
        self.data = defaultdict(lambda: defaultdict(dict))
        self._build_data()

    def _build_occurrence(self, occurence):
        """

        Args:
            occurence: a tuple of class path and primary key

        Returns:
            a tuple of the class and the primary key

        """
        from modeltranslation.utils import build_localized_fieldname
        dotted_path, pk = occurence
        module_name, class_name, field_name = dotted_path.rsplit(".", 2)
        module = importlib.import_module(module_name)
        field_name = build_localized_fieldname(field_name, self.language)

        try:
            model_class = getattr(module, class_name)
        except AttributeError:
            model_class = apps.get_model(module_name, class_name)

        return model_class, field_name, pk

    def _build_data(self):
        """
        Builds the data structure
        """
        for entry in self.po:
            for klass, field, pk in [self._build_occurrence(occur) for occur in entry.occurrences]:
                self.data[klass][pk][field] = entry.msgstr

    def save(self):
        counter = 1
        for klass, table_data in self.data.items():
            for pk, field_data in table_data.items():
                try:
                    instance = klass._default_manager.get(pk=pk)
                    for field_name, field_value in field_data.items():
                        setattr(instance, field_name, field_value)
                    instance.save()
                except klass.DoesNotExist:
                    self.output.write("Object no longer exists in database: id={0}".format(pk))
                    for field_name, field_value in field_data.items():
                        self.output.write(field_name)
                        self.output.write(field_value)
                    self.output.write("-------------------------------------")
                counter += 1
                if counter % 25 == 0 and self.output:
                    self.output.write("{0} rows updated...".format(counter))

        if self.output:
            self.output.write("Finished! {0} rows updated".format(counter))

