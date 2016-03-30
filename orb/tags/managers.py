"""
Manager classes for tag-related models
"""

from django.db import models


class ActiveTagManager(models.Manager):
    """Manager for working only with tags with associated resources"""
    def get_queryset(self):
        return super(ActiveTagManager, self).get_queryset().filter(
            resourcetag__isnull=False,
        ).distinct()