# coding: utf-8

"""
Management command to load country fixtures as tags and tag properties
"""

import os
import csv
import re
from optparse import make_option

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

    option_list = BaseCommand.option_list + (
        make_option("--file",
            dest="fixture",
            default="orb/fixtures/country-codes.csv",
            help="CSV file path"),
        make_option("--name",
            dest="name",
            default="name",
            help="Default column header for country name"),
        make_option("--code",
            dest="code",
            default="ISO3166-1-Alpha-2",
            help="Default column header for country code"),
        make_option("--user",
            dest="user",
            type="int",
            default=1,
            help="Default user to mark as creating"),
    )

    def handle(self, *args, **options):

        try:
            user = User.objects.get(pk=options["user"])
        except User.DoesNotExist:
            raise CommandError("No match user found for '{0}'".format(options["user"]))

        category = Category.objects.filter(name="Geography").first()

        if not os.path.exists(options["fixture"]):
            raise CommandError("Cannot find file '{0}'".format(options["fixture"]))

        name_label = options["name"]
        code_label = options["code"]

        with open(options["fixture"]) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:

                if not has_data(row[code_label]):
                    continue

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
                    self.stderr.write(
                        u"Error: multiple matches for {0}".format(row[name_label]))
                    continue

                if created:
                    self.stdout.write(
                        u"Added new tag: {0}".format(row[name_label]))

                tag_meta, _ = TagProperty.objects.get_or_create(
                    tag=tag, name="code", defaults={"value": row[code_label].upper()})
