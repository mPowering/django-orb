# -*- coding: utf-8 -*-

"""
pytest fixtures
"""

import pytest
from django.contrib.auth.models import User

from orb.models import Category, Tag
from orb.peers.models import Peer
from orb.resources.tests.factory import resource_factory


@pytest.fixture(scope="session")
def test_user():
    user, _ = User.objects.get_or_create(username="tester")
    yield user


@pytest.fixture(scope="session")
def import_user():
    user, _ = User.objects.get_or_create(username="importer")
    yield user



@pytest.fixture(scope="session")
def test_category():
    category, _ = Category.objects.get_or_create(name="test category")
    yield category


@pytest.fixture(scope="session")
def test_tag(test_category, test_user):
    tag, _ = Tag.objects.get_or_create(name="test tag", defaults={
        "category": test_category,
        "create_user": test_user,
        "update_user": test_user,
    })
    yield tag


@pytest.fixture(scope="session")
def test_resource(test_user):
    yield resource_factory(
        user=test_user,
        title=u"Básica salud del recién nacido",
        description=u"Básica salud del recién nacido",
    )


@pytest.fixture(scope="session")
def test_peer():
    peer = Peer.peers.create(name="Distant ORB", host="http://www.orb.org/")
    yield peer


@pytest.fixture(scope="session")
def remote_resource(import_user, test_peer):
    """Fixture for a remotely created resource"""
    yield resource_factory(
        user=import_user,
        title=u"A remote resource",
        description=u"<p>A remote resource</p>",
        source_peer=test_peer,
    )

