# -*- coding: utf-8 -*-

"""
Tests for ORB resource models
"""

import pytest
from django.contrib.auth.models import User
from django.test import TestCase

from orb.models import Resource, ResourceURL
from orb.resources.tests.factory import resource_factory


pytestmark = pytest.mark.django_db


@pytest.fixture(scope="module")
def test_user():
    user, _ = User.objects.get_or_create(username="tester")
    yield user


@pytest.fixture(scope="module")
def test_resource(test_user):
    yield resource_factory(
        user=test_user,
        title=u"Básica salud del recién nacido",
        description=u"Básica salud del recién nacido",
    )


def test_guid(test_resource):
    assert test_resource.guid is not None


def test_languages(test_resource, settings):
    """Instance method should return list of available languages"""
    settings.LANGUAGES = [
        ('en', u'English'),
        ('es', u'Español'),
        ('pt-br', u'Português'),
    ]
    test_resource.title_en = "Hey"
    test_resource.title_pt_br = "Hey"
    test_resource.description_en = "Hey"
    test_resource.description_pt_br = "Hey"
    test_resource.title_es = "hola"
    assert test_resource.available_languages() == ["en", "pt-br"]


class ResourceTests(TestCase):
    """Basic tests of the Resource model and its methods"""

    @classmethod
    def setUpClass(cls):
        cls.user, _ = User.objects.get_or_create(username="tester")
        cls.resource = resource_factory(
            user=cls.user,
            title=u"Básica salud del recién nacido",
            description=u"Básica salud del recién nacido",
        )

    @classmethod
    def tearDownClass(cls):
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
        cls.user, _ = User.objects.get_or_create(username="tester")
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
        User.objects.all().delete()
        Resource.objects.all().delete()

    def test_unicode_display(self):
        """Unicode value of URL is returned"""
        self.assertEqual(
            self.resource_url.__unicode__(),
            u"http://www.example.com/niños",
        )
