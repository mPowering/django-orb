"""
Manager classes for tag-related models
"""

from django.db import models
from django.contrib.auth.models import AnonymousUser
from orb.resources.managers import approved_queryset


class TagQuerySet(models.QuerySet):

    def public(self):
        return self.filter(published=True)

    def active(self):
        return self.filter(resourcetag__isnull=False).distinct()

    def top_level(self):
        return self.filter(category__top_level=True, parent_tag=None).order_by('order_by')

    def approved(self, user=None):
        if user is None:
            user = AnonymousUser()
        return approved_queryset(self.active(), user, relation="resourcetag__resource__")


class ResourceTagManager(models.Manager):
    """Manager for the ResourceTag linking model"""

    def approved(self, user=None):
        """
        Queryset that includes only resource tags with resources viewable by
        given user based on approval state.

        Args:
            user (auth.User): the user to check 'permission' against

        Returns:
            QuerySet: A queryset filtered by status and/or user

        """
        qs = super(ResourceTagManager, self).get_queryset()
        if user is None:
            user = AnonymousUser()
        return approved_queryset(qs, user, relation="resource__")
