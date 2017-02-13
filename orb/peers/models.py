"""
Models for the ORB content sharing network
"""
import logging
from collections import defaultdict

from django.db import models
from django.db.models import Q
from django.utils.functional import cached_property
from django.utils.timezone import now
from orb_api.api import OrbClient

logger = logging.getLogger('orb')


class PeersQuerySet(models.QuerySet):
    def active(self):
        return self.filter(active=True)

    def inactive(self):
        return self.filter(active=False)

    def queryable(self):
        """Returns only peers which can be queried by API"""
        return self.active().filter(api_user__isnull=False, api_key__isnull=False)

    def unqueryable(self):
        """Returns only peers which cannot be queried by API"""
        return self.filter(Q(active=False) | Q(api_user__isnull=True) | Q(api_key__isnull=True))


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

    @cached_property
    def client(self):
        return OrbClient(self.host, self.api_user, self.api_key, sleep=1)

    def sync_resources(self, writer=None):
        """
        Interface method to query and sync resources from the peer

        Args:
            writer: optional output writing function

        Returns:
            dictionary of results

        """
        from orb.models import Resource
        log_entry = self.logs.create()
        # Does resource exist locally?
        # If yes - do update?
        # If it was here but was rejected, make it pending
        # If no, create

        def default_writer(value):
            print(value)

        resource_counts = defaultdict(lambda: 0)

        if writer is None:
            writer = default_writer

        try:
            last_update = self.logs.latest().finished
        except PeerQueryLog.DoesNotExist:
            last_update = None

        filters = {} if last_update is None else {'updated__gte': last_update}

        total_count, resource_list = self.client.list_resources(**filters)

        for api_resource in resource_list:
            try:
                local_resource = Resource.resources.get(guid=api_resource['guid'])
            except Resource.DoesNotExist:
                Resource.create_from_api(api_resource)
                resource_counts['new_resources'] += 1
                writer(u"Created a new resource: {}".format(api_resource['title']))
            else:
                if local_resource.is_local():
                    resource_counts['skipped_local_resources'] += 1
                else:
                    was_updated = local_resource.update_from_api(api_resource)
                    if was_updated:
                        resource_counts['updated_resources'] += 1
                    else:
                        resource_counts['unchanged_resources'] += 1

        # TODO add JSON field for results
        log_entry.finish()
        return resource_counts


class PeerQueryLog(models.Model):
    """
    Model to log when a peer is queried for update and when the update finishes
    """

    created = models.DateTimeField(editable=False, default=now)
    finished = models.DateTimeField(null=True, blank=True, editable=False)
    peer = models.ForeignKey('Peer', related_name='logs')

    entries = models.Manager()
    objects = entries

    class Meta:
        get_latest_by = 'finished'

    def __unicode__(self):
        return u"{} - {}".format(self.peer, self.created)

    def finish(self):
        """
        Interface for updating the completion (finished) time

        Saves the model instance
        """
        self.finished = now()
        self.save()
