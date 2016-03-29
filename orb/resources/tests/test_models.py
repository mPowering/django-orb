# -*- coding: utf-8 -*-

"""
Tests for ORB resource models
"""

from django.contrib.auth.models import User
from django.test import TestCase

from orb.models import ResourceURL
from orb.resources.tests.factory import resource_factory


class ResourceTests(TestCase):
    """Basic tests of the Resource model and its methods"""

    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create(username="tester")
        cls.resource = resource_factory(
            user=cls.user,
            title=u"Básica salud del recién nacido",
            description=u"Básica salud del recién nacido",
        )

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()
        cls.resource.delete()

    def test_absolute_url(self):
        """URL is returned with slug"""
        self.assertEqual(
            self.resource.get_absolute_url(),
            "/resource/view/basica-salud-del-recien-nacido"
        )

    def test_unicode_display(self):
        """Unicode value of title is returned"""
        self.assertEqual(
            self.resource.__unicode__(),
            u"Básica salud del recién nacido",
        )

    def test_unique_slugification(self):
        """Unique slug is generated for new resources"""
        duplicate = resource_factory(
            user=self.user,
            title=u"Básica salud del recién nacido",
            description=u"Básica salud del recién nacido",
        )
        self.assertEqual(
            self.resource.slug,
            "basica-salud-del-recien-nacido"
        )
        self.assertEqual(
            duplicate.slug,
            "basica-salud-del-recien-nacido-2"
        )


class ResourceURLTests(TestCase):
    """Basic tests of the ResourceURL model and its methods"""

    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create(username="tester")
        cls.resource = resource_factory(
            user=cls.user,
            title=u"Básica salud del recién nacido",
            description=u"Básica salud del recién nacido",
        )
        cls.resource_url = ResourceURL.objects.create(
            resource=cls.resource,
            url=u"http://www.example.com/niños",
            create_user=cls.user,
            update_user=cls.user,
        )

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()
        cls.resource.delete()
        cls.resource_url.delete()

    def test_unicode_display(self):
        """Unicode value of URL is returned"""
        self.assertEqual(
            self.resource_url.__unicode__(),
            u"http://www.example.com/niños",
        )
