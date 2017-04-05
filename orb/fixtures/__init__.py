# -*- coding: utf-8 -*-

"""
pytest fixtures
"""

import pytest
from django.contrib.auth.models import User

from orb.models import Category, Tag
from orb.peers.models import Peer
from orb.resources.tests.factory import resource_factory

pytestmark = pytest.mark.django_db


@pytest.fixture
def testing_user():
    user, _ = User.objects.get_or_create(username="tester")
    yield user


@pytest.fixture(scope="session")
def import_user():
    user, _ = User.objects.get_or_create(username="importer")
    yield user


@pytest.fixture
def sample_category():
    category, _ = Category.objects.get_or_create(name="test category")
    yield category


@pytest.fixture
def sample_tag(sample_category, testing_user):
    tag, _ = Tag.objects.get_or_create(name="test tag", defaults={
        "category": sample_category,
        "create_user": testing_user,
        "update_user": testing_user,
    })
    yield tag


@pytest.fixture
def test_resource(testing_user):
    yield resource_factory(
        user=testing_user,
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

