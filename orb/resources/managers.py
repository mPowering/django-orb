"""
Manager classes for resource-related models
"""

from django.contrib.auth.models import AnonymousUser
from django.db import models


def approved_queryset(queryset, user=AnonymousUser, status="approved"):
    """
    Filters the given queryset based on the allowed status and user

    This function is intended to be used via the interface of a Manager method

    Args:
        queryset: the initial queryset
        user: the accessing User
        status: string matching the required status level

    Returns:
        QuerySet: A queryset filtered by status and/or user

    """
    if user == AnonymousUser:
        return queryset.filter(status=status)
    if user.is_staff:
        return queryset
    try:
        if user.userprofile.mep_member or user.userprofile.crt_member:
            return queryset
    except AttributeError:
        pass

    return queryset.filter(
        models.Q(status=status) |
        models.Q(create_user=user) |
        models.Q(update_user=user)
    )


class ResourceManager(models.Manager):

    def approved(self, user=AnonymousUser):
        """
        Queryset that includes only resources viewable by given user

        Args:
            user (auth.User): the user to check 'permission' against

        Returns:
            QuerySet: A queryset filtered by status and/or user

        """
        qs = super(ResourceManager, self).get_queryset()
        return approved_queryset(qs, user)


class ApprovedManager(models.Manager):

    def __init__(self, *args, **kwargs):
        self.user = AnonymousUser
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
