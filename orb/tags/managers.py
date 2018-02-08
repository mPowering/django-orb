"""
Manager classes for tag-related models
"""
from __future__ import unicode_literals

from django.contrib.auth.models import AnonymousUser
from django.db import models

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

    def by_resource(self, resource):
        """
        Returns a queryset related to the specific resource

        Ordering is preserved against the order in which the association between
        each tag and the resource was added.
        """
        return self.filter(resourcetag__resource=resource).order_by('resourcetag__id')

    def by_category(self, category_slug):
        """"""
        return self.filter(category__slug=category_slug)

    def roles(self):
        return self.filter(category__slug='audience').order_by('order_by', 'name')

    def choices(self, empty_label=''):
        """Returns a generator of choice tuples from queryset (using ID)

        Args:
            empty_label: optional label for empty label. If included an empty label
                        and separator will be included

        Returns:
            generator of choice tuples using primary key
        """
        if empty_label:
            yield ('', empty_label)
            yield ('', '---')
        for t in self:
            yield t.id, t.name

    def slugchoices(self, empty_label=''):
        """Returns a generator of choice tuples from queryset (using slug)

        Args:
            empty_label: optional label for empty label. If included an empty label
                        and separator will be included

        Returns:
            generator of choice tuples using slug
        """
        if empty_label:
            yield ('', empty_label)
            yield ('', '---')
        for t in self:
            yield t.slug, t.name


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
