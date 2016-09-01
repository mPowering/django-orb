# -*- coding: utf-8 -*-

"""
Management command that generates a PO file for a specified language
based on django-modeltranslation fields.

This generates a quasi-complete PO file, in that it cannot be turned
into a usable compiled MO file.

Use polib to

We want a graph of

This example::

    #: myapp.MyModel.name:300 myapp.OtherModel.title:12
    msgid "Advanced search"
    msgstr "Búsqueda avanzada"

Would find occcurences of the string "Advanced search" in the `name` field
of the MyModel model (in the `myapp` app), in the instance with primary key
value of 12, and also in the `title` field of the `OtherModel` model for
primary key 12.

"""
import IPython
from collections import defaultdict
from django.conf import settings
from django.core.management.base import BaseCommand
from modeltranslation.translator import translator
import importlib
from modeltranslation_exim import DatabaseTranslations


def get_installed(*dotted_paths):
    """

    Args:
        *dotted_paths:

    Returns:

    """


def get_strings_for_model(model, fields):
    """

    Args:
        model:
        fields:

    Returns:

    """


class Command(BaseCommand):
    """
    Exports translatable database fields to a PO file format

    By default it should only return PO files for languages that
    are in the site LANGUAGES. To force an additional language
    should require an optional flag.

    This should also only optionally depend on modeltranslation
    for export, as it may be the case that you want to export
    database content before modeltranslation has been added.
    To that end, importing the translator should be used if and
    only if the model/field names have not been specified in the
    command arguments.
    """

    def handle(self, *args, **options):
        from django.apps import apps
        class_and_field = defaultdict(list)
        for dotted_path in args:
            module_name, class_name, field_name = dotted_path.rsplit(".", 2)

            module = importlib.import_module(module_name)

            try:
                model_class = getattr(module, class_name)
            except AttributeError:
                model_class = apps.get_model(module_name, class_name)

            class_and_field[model_class].append(field_name)

        exported = DatabaseTranslations(class_and_field)
        exported.save()


    def blah(self):
        translated_models = translator.get_registered_models()
        print(settings.LANGUAGES)
        print(settings.LANGUAGE_CODE)
        print(settings.MODELTRANSLATION_DEFAULT_LANGUAGE)

        for model in translated_models:
            fields = translator.get_options_for_model(model)
            print(fields)
            print(dir(fields))
            print(fields.fields)
            for fld in fields.fields:
                print(dir(fld))
            for instance in model._default_manager.all():
                pass
                #for field in fields:
                #    print(getattr(instance, field))
                #print(instance)

        IPython.embed()
