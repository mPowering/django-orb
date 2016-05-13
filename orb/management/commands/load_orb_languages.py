"""
Management command to load language fixtures as tags
"""
import os
import csv
import re
from optparse import make_option

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from orb.models import Category, Tag


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
    help = "Loads languages from CSV fixtures into tag database"

    option_list = BaseCommand.option_list + (
        make_option("--file",
            dest="fixture",
            default="orb/fixtures/iso639.csv",
            help="CSV file path"),
        make_option("--image",
            dest="image",
            default="tag/language_default.png",
            help="Default image (static image path)"),
        make_option("--user",
            dest="user",
            type="int",
            default=1,
            help="Default user to mark as creating"),
        make_option("--iso6392",
            action="store_true",
            dest="iso6392",
            default=False,
            help="Flag for including all ISO 639.2 (only ISO 639.1 included by default)"),
    )

    def handle(self, *args, **options):

        try:
            user = User.objects.get(pk=options["user"])
        except User.DoesNotExist:
            raise CommandError("No match user found for '{0}'".format(options["user"]))

        category = Category.objects.filter(name="Language").first()

        if not os.path.exists(options["fixture"]):
            raise CommandError("Cannot find file '{0}'".format(options["fixture"]))

        with open(options["fixture"]) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:

                if not options["iso6392"] and not has_data(row["iso639-1"]):
                    continue

                tag, _ = Tag.objects.get_or_create(name=row["English"], defaults={
                    "create_user": user,
                    "update_user": user,
                    "category": category,
                    "image": options["image"],
                })
