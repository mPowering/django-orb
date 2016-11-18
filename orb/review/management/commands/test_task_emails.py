"""
This is a debugging command designed to test emails on the system
"""

from django.core.management.base import BaseCommand, CommandError

from orb.review import tasks
from orb.review.models import ContentReview
from orb.models import Resource
from django.conf import settings


class Command(BaseCommand):
    help = 'Checks for pending reviews and sends a reminder to the reviewer'

    def handle(self, *args, **options):
        if settings.EMAIL_BACKEND != 'django.core.mail.backends.console.EmailBackend':
            # Guard against accidentally sending out emails
            raise CommandError("You are using the '{}' email backend."
                               "This command only runs using the console.EmailBackend.".format(settings.EMAIL_BACKEND))

        task_names = {
            'review_assignment': (tasks.send_review_assignment_email, ContentReview.reviews.all().first),
            'review_reminder': (tasks.send_review_reminder_email, ContentReview.reviews.all().first),
            'resource_approved': (tasks.send_resource_approved_email, Resource.objects.all().first)
        }

        for arg in args:
            try:
                function, callable = task_names[arg]
            except ValueError as exc:
                raise CommandError("Ooops: {}".format(exc))

            self.stdout.write("Calling '{0}' using {1}".format(function, callable()))

            function(callable())


