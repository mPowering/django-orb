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
import importlib
import polib
from collections import defaultdict

from django.apps import apps
from django.core.management.base import BaseCommand, CommandError
from optparse import make_option

from modeltranslation_exim import POTranslations


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
    help = "Update database translations from specially formatted PO file"
    args = "<PO file path>"

    option_list = BaseCommand.option_list + (
        make_option('--language',
            dest='language',
            help='Language code for target language, e.g. `pt-br` (required)',),
    )

    def handle(self, *args, **options):
        try:
            filepath, = args
        except ValueError:
            raise CommandError("Command takes one required file path argument")

        language = options.get('language')
        if language is None:
            raise CommandError("Missing required --language option")

        translator = POTranslations(filepath, language, output=self.stdout)
        translator.save()

