# -*- coding: utf-8 -*-

"""
Tests for ORB resource models
"""

import pytest
from django.contrib.auth.models import User

from orb.models import ResourceURL
from orb.peers.models import Peer
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


@pytest.fixture(scope="module")
def test_peer():
    yield Peer.peers.create(name="Distant ORB", host="http://www.orb.org/")


class TestResource(object):

    def test_guid(self, test_resource):
        assert test_resource.guid is not None

    def test_absolute_url(self, test_resource):
        """URL is returned with slug"""
        assert test_resource.get_absolute_url() == "/resource/view/basica-salud-del-recien-nacido"

    def test_unicode_display(self, test_resource):
        """Unicode value of title is returned"""
        assert test_resource.__unicode__() == u"Básica salud del recién nacido"

    def test_non_latin_slugification(self, admin_user):
        """Non-latin characters should be transliterated"""
        test_user = admin_user
        cyrillic_resource= resource_factory(
            user=test_user,
            title=u"Санкт-Петербург Питоны",  # Saint Petersburg Pythons
            description=u"Some resource",
        )
        assert cyrillic_resource.slug == u"sankt-peterburg-pitony"

        chinese_resource= resource_factory(
            user=test_user,
            title=u"北京蟒蛇",  # Beijing Pythons
            description=u"Some resource",
        )
        assert chinese_resource.slug == u"bei-jing-mang-she"

    def test_unique_slugification(self, admin_user):
        """Unique slug is generated for new resources"""
        test_user = admin_user
        original = resource_factory(
            user=test_user,
            title=u"Básica salud del recién nacido",
            description=u"Básica salud del recién nacido",
        )
        duplicate = resource_factory(
            user=test_user,
            title=u"Básica salud del recién nacido",
            description=u"Básica salud del recién nacido",
        )
        assert original.slug == "basica-salud-del-recien-nacido"
        assert original.slug != duplicate.slug
        assert duplicate.slug == "basica-salud-del-recien-nacido-2"

    def test_languages(self, test_resource, settings):
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


class TestResourceURL(object):

    def test_unicode_display(self):
        """Unicode value of URL is returned"""
        assert ResourceURL(url=u"http://www.example.com/niños").__unicode__() == u"http://www.example.com/niños"


class TestResourceLocality(object):

    def test_local_resource(self, test_resource):
        assert test_resource.is_local()

    def test_downloaded_resource(self, test_resource, test_peer):
        """A source peer should mark a resource as not local"""
        test_resource.source_peer = test_peer
        assert not test_resource.is_local()

    def test_sourced_resource(self, test_resource):
        """Both a source name and host should mark a resource as not local"""
        test_resource.source_name = "Another ORB"
        test_resource.source_host = "http://www.yahoo.com"
        assert not test_resource.is_local()
