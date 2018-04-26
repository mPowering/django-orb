# coding: utf-8

"""
Management command to load country fixtures as tags and tag properties
"""

from __future__ import unicode_literals

import csv
import os
import re

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError

from orb.models import Category, Tag, TagProperty


def has_data(input):
    """Identify if the input contains any meaningful string content

    CSV input may include non-breaking space which is a Unicode character,
    however the csv module does not handle unicode.

    Args:
        input: string value

    Returns:
        bool

    """
    input = input.replace("\xc2\xa0", " ")
    return bool(re.compile("\S").match(input))


class Command(BaseCommand):
    help = "Loads countries from CSV fixtures into tag database"

    def add_arguments(self, parser):
        parser.add_argument(
            "--file",
            dest="fixture",
            default="orb/fixtures/country-codes.csv",
            help="CSV file path",
        )
        parser.add_argument(
            "--name",
            dest="name",
            default="name",
            help="Default column header for country name",
        )
        parser.add_argument(
            "--code",
            dest="code",
            default="ISO3166-1-Alpha-2",
            help="Default column header for country code",
        )
        parser.add_argument(
            "--user",
            dest="user",
            type=int,
            default=1,
            help="Default user to mark as creating",
        )

    def handle(self, *args, **options):

        try:
            user = User.objects.get(pk=options[b"user"])
        except User.DoesNotExist:
            raise CommandError("No match user found for '{0}'".format(options[b"user"]))

        category, _ = Category.objects.get_or_create(name="Geography", defaults={
            'top_level': True,
        })

        if not os.path.exists(options[b"fixture"]):
            raise CommandError("Cannot find file '{0}'".format(options[b"fixture"]))

        name_label = options[b"name"]
        code_label = options[b"code"]

        with open(options[b"fixture"]) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:

                if not has_data(row[code_label]):
                    continue

                row = {k: v.decode('utf-8') for k, v in row.items()}

                try:
                    tag, created = Tag.objects.get_or_create(
                        name=row[name_label], defaults={
                            "create_user": user,
                            "update_user": user,
                            "category": category,
                            "image": "tag/geography_default.png",
                        }
                    )
                except Tag.MultipleObjectsReturned:
                    self.stderr.write("Error: multiple matches for '{0}'".format(row[name_label]))
                    continue

                if created:
                    self.stdout.write("Added new tag: '{0}'".format(row[name_label]))

                tag_meta, _ = TagProperty.objects.get_or_create(
                    tag=tag, name="code", defaults={"value": row[code_label].upper()})
