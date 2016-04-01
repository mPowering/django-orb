"""
Manager classes for tag-related models
"""

from django.db import models
from django.contrib.auth.models import AnonymousUser
from orb.resources.managers import approved_queryset


class ActiveTagManager(models.Manager):
    """Manager for working only with tags with associated resources"""

    def get_queryset(self):
        return super(ActiveTagManager, self).get_queryset().filter(
            resourcetag__isnull=False,
        ).distinct()

    def approved(self, user=None):
        """
        Queryset that includes only tags with resources viewable by given user
        based on approval state.

        Args:
            user (auth.User): the user to check 'permission' against

        Returns:
            QuerySet: A queryset filtered by status and/or user

        """
        qs = super(ActiveTagManager, self).get_queryset()
        if user is None:
            user = AnonymousUser()
        return approved_queryset(qs, user, relation="resourcetag__resource__")


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
