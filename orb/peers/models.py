"""
Models for the ORB content sharing network
"""
import logging

from django.db import models
from django.utils.timezone import now

logger = logging.getLogger('orb')


class PeersQuerySet(models.QuerySet):
    def active(self):
        return self.filter(active=True)

    def inactive(self):
        return self.filter(active=False)

    def queryable(self):
        """Returns only peers which can be queried by API"""
        return self.active().filter(api_user__isnull=False, api_key__isnull=False)


class Peer(models.Model):
    """
    A peer ORB node
    """
    name = models.CharField(max_length=100)
    host = models.URLField()
    active = models.BooleanField(default=True)
    api_user = models.CharField(max_length=100, blank=True, null=True)
    api_key = models.CharField(max_length=100, blank=True, null=True)

    peers = PeersQuerySet.as_manager()
    objects = peers

    def __unicode__(self):
        return self.name

    def sync_resources(self, writer=None):
        """
        Interface method to query and sync resources from the peer

        Args:
            writer: optional output writing function

        Returns:
            dictionary of results

        """


class PeerQueryLog(models.Model):
    """
    Model to log when a peer is queried for update and when the update finishes
    """

    created = models.DateTimeField(editable=False, default=now)
    finished = models.DateTimeField(null=True, blank=True, editable=False)
    peer = models.ForeignKey('Peer', related_name='logs')

    def finish(self):
        """
        Interface for updating the completion (finished) time

        Saves the model instance
        """
        self.finished = now()
        self.save()
