"""
Management command to add a superuser with CLI args including UserProfile

This should only be used to programmatically create superusers with *initial*
passwords, to be changed after creation.

Usage:

    django-admin.py add_super_user --email="someone@hello.com" --password="COOLPASSWORD"

"""

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from orb.models import UserProfile


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            '--email',
            dest='email',
            help='Email address',
            required=True,
        )
        parser.add_argument(
            '--password',
            dest='password',
            help='Initial password',
            required=True,
        )

    def handle(self, *args, **options):

        username = options.get('email')

        try:
            user = get_user_model().objects.get(username=username)
        except get_user_model().DoesNotExist:
            user = get_user_model().objects.create_superuser(
                username,
                password=options.get('password'),
                email=options.get('email'),
            )
            UserProfile.objects.create(user=user)
            self.stdout.write("Create new user '{}'".format(username))
        else:
            self.stdout.write("Found existing user '{}'".format(username))

