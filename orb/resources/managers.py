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

        return qs.filter(models.Q(status=APPROVED) | models.Q(create_user=user))
