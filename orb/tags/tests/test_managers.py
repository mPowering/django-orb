"""
Tests for orb.tags.managers.
"""

from django.contrib.auth.models import User
from django.test import TestCase

from orb.models import Category, Resource, Tag, ResourceTag


def resource_fixture(**kwargs):
    user = kwargs.pop("user", None)
    if user:
        kwargs.update({
            "create_user": user,
            "update_user": user,
        })

    defaults = {
        "title": "Test resource",
        "description": "Test resource",
    }
    defaults.update(kwargs)
    return Resource.objects.create(**defaults)


def category_fixture(**kwargs):
    defaults = {
        "name": "Test category",
    }
    defaults.update(kwargs)
    return Category.objects.create(**defaults)


def tag_fixture(**kwargs):
    user = kwargs.pop("user", None)
    if user:
        kwargs.update({
            "create_user": user,
            "update_user": user,
        })

    defaults = {
        "category": category_fixture(),
        "name": "Test tag",
    }
    defaults.update(kwargs)
    return Tag.objects.create(**defaults)


class ActiveManagerTests(TestCase):
    """
    Tests for the active manager class.

    The active manager only returns tags with associated resources
    """

    @classmethod
    def setUpClass(cls):
        user = User.objects.create(username="McTester")
        resource = resource_fixture(user=user)
        second_resource= resource_fixture(user=user)
        used_tag = tag_fixture(user=user)
        unused_tag = tag_fixture(user=user)  # noqa
        ResourceTag.objects.create(create_user=user, tag=used_tag, resource=resource)
        ResourceTag.objects.create(create_user=user, tag=used_tag, resource=second_resource)

    def test_default_manager(self):
        self.assertEqual(Tag.objects.all().count(), 2)

    def test_active_manager(self):
        self.assertEqual(Tag.active.all().count(), 1)


