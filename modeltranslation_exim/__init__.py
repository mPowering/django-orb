# -*- coding: utf-8 -*-

import sys
from collections import defaultdict

import polib
from modeltranslation.utils import build_localized_fieldname


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
