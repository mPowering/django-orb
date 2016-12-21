"""
Management command to list ORB peer data

Usage:

    $ django-admin.py list_peers

      [1] Malawi ORB, https://www.malawi-orb.org
      [2] ORB Pakistan, https://www.orb.pk

"""

from django.core.management.base import BaseCommand

from orb.peers.models import Peer


class Command(BaseCommand):

    def handle(self, *args, **options):
        active = Peer.peers.queryable()
        inactive = Peer.peers.inactive()

        if not active or inactive:
            print("No peers have been registered.")

        if active:
            print("\nQueryable peers\n")
            for peer in active:
                print("[{}] {}, {}".format(peer.pk, peer.name, peer.host))

        if inactive:
            print("\nUnqueryable peers (unsynced)\n")
            for peer in inactive:
                print("[{}] {}, {}".format(peer.pk, peer.name, peer.host))
