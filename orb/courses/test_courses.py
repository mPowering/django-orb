"""
Tests for the courses app
"""

from __future__ import unicode_literals

import json

import pytest
from django.core.urlresolvers import reverse

from orb.tests.utils import login_client
from orb.courses import forms
from orb.courses import models


@pytest.fixture
def course(testing_user):
    yield models.Course.courses.create(
        create_user=testing_user,
        update_user=testing_user,
        title="My first course",
    )


def test_anon_users(client):
    response = client.get(reverse('courses_list'))
    assert response.status_code == 302


def test_authd_users(admin_client):
    response = admin_client.get(reverse('courses_list'))
    assert response.status_code == 200


def test_form_valid_json_data(admin_user):
    form = forms.CourseForm(data={'sections': '[]', 'title': 'Hello World'})
    assert form.is_valid()


def test_form_invalid_json_data(admin_user):
    form = forms.CourseForm(data={'sections': '["hello": "oka"]', 'title': 'Hello World'})
    assert not form.is_valid()


@pytest.mark.django_db
def test_admin_can_edit_course(course, admin_client, rf):
    response = admin_client.get(reverse('courses_edit', kwargs={'pk': course.pk}))
    assert response.status_code == 200

    response = admin_client.post(
        reverse('courses_edit', kwargs={'pk': course.pk}),
        {'sections': '[]', 'title': 'Hello'},
    )
    assert response.status_code == 200


@pytest.mark.django_db
def test_owner_can_edit_course(testing_profile, client):
    with login_client(client, username='tester', password='password'):
        response = client.get(reverse('courses_edit', kwargs={'pk': course.pk}))
        assert response.status_code == 200

        response = client.post(
            reverse('courses_edit', kwargs={'pk': course.pk}),
            json.dumps({'sections': '[]', 'title': 'Hello'}),
            content_type="application/json",
        )
        assert response.status_code == 200


@pytest.mark.django_db
def test_non_owner_cannot_edit_course(importer_profile, client):
    with login_client(client, username='tester', password='password'):
        response = client.get(reverse('courses_edit', kwargs={'pk': course.pk}))
        assert response.status_code == 200

        response = client.post(
            reverse('courses_edit', kwargs={'pk': course.pk}),
            json.dumps({'sections': '[]', 'title': 'Hello'}),
            content_type="application/json",
        )
        assert response.status_code == 403
