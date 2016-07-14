# -*- coding: utf-8 -*-

"""
Tests for ORB resource models
"""

from django.contrib.auth.models import User
from django.test import TestCase

from orb.models import Resource, ResourceURL
from orb.resources.tests.factory import resource_factory


class ResourceTests(TestCase):
    """Basic tests of the Resource model and its methods"""

    @classmethod
    def setUpClass(cls):
        super(ResourceTests, cls).setUpClass()
        cls.user = User.objects.create(username="tester")
        cls.resource = resource_factory(
            user=cls.user,
            title=u"Básica salud del recién nacido",
            description=u"Básica salud del recién nacido",
        )

    @classmethod
    def tearDownClass(cls):
        super(ResourceTests, cls).tearDownClass()
        User.objects.all().delete()
        Resource.objects.all().delete()

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

    def test_non_latin_slugification(self):
        """Non-latin characters should be transliterated"""
        cyrillic_resource= resource_factory(
            user=self.user,
            title=u"Санкт-Петербург Питоны",  # Saint Petersburg Pythons
            description=u"Some resource",
        )
        self.assertEqual(cyrillic_resource.slug, u"sankt-peterburg-pitony")

        chinese_resource= resource_factory(
            user=self.user,
            title=u"北京蟒蛇",  # Beijing Pythons
            description=u"Some resource",
        )
        self.assertEqual(chinese_resource.slug, u"bei-jing-mang-she")


class ResourceURLTests(TestCase):
    """Basic tests of the ResourceURL model and its methods"""

    @classmethod
    def setUpClass(cls):
        super(ResourceURLTests, cls).setUpClass()
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
        super(ResourceURLTests, cls).tearDownClass()
        User.objects.all().delete()
        Resource.objects.all().delete()

    def test_unicode_display(self):
        """Unicode value of URL is returned"""
        self.assertEqual(
            self.resource_url.__unicode__(),
            u"http://www.example.com/niños",
        )
