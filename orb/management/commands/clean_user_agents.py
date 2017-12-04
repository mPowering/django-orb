
"""
Management command to remove bots/crawlers from trackers
"""

from optparse import make_option

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError

from orb.models import ResourceTracker, SearchTracker, TagTracker
from orb.lib import search_crawler

class Command(BaseCommand):
    help = "Removes bots/crawlers from trackers"


    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        # ResourceTracker
        rts = ResourceTracker.objects.all()
        for rt in rts:
            if search_crawler.is_search_crawler(rt.user_agent):
                print "found: " + rt.user_agent
                rt.delete()
            

        # SearchTracker
        # @TODO    
            