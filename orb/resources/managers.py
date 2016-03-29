"""
Manager classes for resource-related models
"""

from django.contrib.auth.models import AnonymousUser
from django.db import models


class ResourceManager(models.Manager):

    def approved(self, user=AnonymousUser):
        """
        Queryset that includes

        Args:
            user (auth.User): the user to check 'permission' against

        Returns:
            QuerySet: A queryset filtered by status and/or user

        """
        APPROVED = "approved"  # noqa; redefined to avoid circular import
        qs = super(ResourceManager, self).get_queryset()

        if user == AnonymousUser:
            return qs.filter(status=APPROVED)
        if user.is_staff:
            return qs

        return qs.filter(
            models.Q(status=APPROVED) |
            models.Q(create_user=user) |
            models.Q(update_user=user)
        )


class ApprovedManager(models.Manager):

    def __init__(self, *args, **kwargs):
        self.user = AnonymousUser
        super(ApprovedManager, self).__init__(*args, **kwargs)

    def get_queryset(self, user=None):
        """
        Queryset that includes

        Args:
            user (auth.User): the user to check 'permission' against

        Returns:
            QuerySet: A queryset filtered by status and/or user

        """
        APPROVED = "approved"  # noqa; redefined to avoid circular import
        qs = super(ApprovedManager, self).get_queryset()

        if user is not None:
            self.user = user

        if self.user == AnonymousUser:
            return qs.filter(status=APPROVED)
        if self.user.is_staff:
            return qs

        return qs.filter(
            models.Q(status=APPROVED) |
            models.Q(create_user=self.user) |
            models.Q(update_user=self.user)
        )

    def filter(self, **kwargs):
        user = kwargs.pop('user', AnonymousUser)
        self.user = user
        return super(ApprovedManager, self).filter(**kwargs)

    def get(self, **kwargs):
        user = kwargs.pop('user', AnonymousUser)
        self.user = user
        return super(ApprovedManager, self).get(**kwargs)
