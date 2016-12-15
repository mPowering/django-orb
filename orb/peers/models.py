"""
Models for the ORB content sharing network
"""
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import now


class PeersQuerySet(models.QuerySet):
    def active(self):
        return self.filter(active=True)


class Peer(models.Model):
    """
    A peer ORB node
    """
    name = models.CharField(max_length=100)
    host = models.URLField()
    active = models.BooleanField(default=True)

    peers = PeersQuerySet.as_manager()
    objects = peers

    def __unicode__(self):
        return self.name


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
