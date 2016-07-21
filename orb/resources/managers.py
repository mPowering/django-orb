"""
Manager classes for resource-related models
"""

from django.contrib.auth.models import AnonymousUser
from django.db import models


def approved_queryset(queryset, user=AnonymousUser, status="approved", relation=""):
    """
    Filters the given queryset based on the allowed status and user

    This function is intended to be used via the interface of a Manager method

    Args:
        queryset: the initial queryset
        user: the accessing User
        status: string matching the required status level
        relation: a string describing a Django ORM relation lookup for filtering
                objects that are related to Resources. By defaul this will search
                against Resources directly

    Returns:
        QuerySet: A queryset filtered by status and/or user

    """
    queryset = queryset.exclude(**{"{0}status".format(relation): "rejected"})

    status_filter = {"{0}status".format(relation): status}
    creator_filter = {"{0}create_user".format(relation): user}
    updater_filter = {"{0}update_user".format(relation): user}

    if not user.is_authenticated():
        return queryset.filter(**status_filter)
    if user.is_staff:
        return queryset
    try:
        if user.userprofile.is_reviewer:
            return queryset
    except AttributeError:
        pass

    return queryset.filter(
        models.Q(**status_filter) |
        models.Q(**creator_filter) |
        models.Q(**updater_filter)
    )


class ResourceManager(models.Manager):

    def approved(self, user=None):
        """
        Queryset that includes only resources viewable by given user
        based on approval state.

        Args:
            user (auth.User): the user to check 'permission' against

        Returns:
            QuerySet: A queryset filtered by status and/or user

        """
        qs = super(ResourceManager, self).get_queryset()
        if user is None:
            user = AnonymousUser()
        return approved_queryset(qs, user)

    def pending(self):
        return self.get_queryset().exclude(
            models.Q(status="approved") |
            models.Q(status="rejected")
        )


class ResourceURLManager(models.Manager):

    def approved(self, user=None):
        """
        Queryset that includes only resource URLs viewable by given user
        based on approval state.

        Args:
            user (auth.User): the user to check 'permission' against

        Returns:
            QuerySet: A queryset filtered by status and/or user

        """
        qs = super(ResourceURLManager, self).get_queryset()
        if user is None:
            user = AnonymousUser()
        return approved_queryset(qs, user, relation="resource__")


class ApprovedManager(models.Manager):

    def __init__(self, *args, **kwargs):
        self.user = AnonymousUser()
        super(ApprovedManager, self).__init__(*args, **kwargs)

    def get_queryset(self, user=None):
        """
        Queryset that includes only resources viewable by given user

        Args:
            user (auth.User): the user to check 'permission' against

        Returns:
            QuerySet: A queryset filtered by status and/or user

        """
        qs = super(ApprovedManager, self).get_queryset()
        if user is None:
            user = self.user

        return approved_queryset(qs, user)

    def filter(self, **kwargs):
        user = kwargs.pop('user', AnonymousUser)
        self.user = user
        return super(ApprovedManager, self).filter(**kwargs)

    def get(self, **kwargs):
        user = kwargs.pop('user', AnonymousUser)
        self.user = user
        return super(ApprovedManager, self).get(**kwargs)
