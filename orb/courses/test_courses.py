# -*- coding: utf-8 -*-

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
    assert response.status_code == 200


def test_authd_users(admin_client):
    response = admin_client.get(reverse('courses_list'))
    assert response.status_code == 200


def test_form_valid_json_data(admin_user):
    form = forms.CourseForm(data={'sections': '[]', 'title': 'Hello World'})
    assert form.is_valid()


def test_form_invalid_json_data(admin_user):
    form = forms.CourseForm(data={'sections': '["hello": "oka"]', 'title': 'Hello World'})
    assert not form.is_valid()


def test_save_course_form(admin_user, testing_user):
    form = forms.CourseForm(user=admin_user, data={'sections': '[]', 'title': 'Hello World'})
    assert form.is_valid()
    course = form.save()

    assert course.create_user == course.update_user == admin_user

    form = forms.CourseForm(user=testing_user, data={'sections': '[]', 'title': 'Hello World'}, instance=course)
    assert form.is_valid()
    course = form.save()
    assert course.create_user == admin_user
    assert course.update_user == testing_user


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


def test_moodle_name():
    course = models.Course(title="Thé Best Course")
    assert course.moodle_file_name == "the-best-course-backup.mbz"


def test_section_data():
    data = [{
        "resources": [{
            "type": "CourseActivity",
            "description": "Hello world",
            "title": "First slide"
        }, {
            "type": "CourseActivity",
            "description": "Olé!",
            "title": "Intermission"
        }]
    }, {
        "resources": [{
            "type": "CourseActivity",
            "description": "Second section description",
            "title": "Second section title"
        }]
    }]
    course = models.Course(sections=json.dumps(data))
    assert course.section_data() == data


def test_moodle_activities():
    data = [{
        "resources": [{
            "type": "CourseActivity",
            "description": "Hello world",
            "title": "First slide"
        }, {
            "type": "CourseActivity",
            "description": "Olé!",
            "title": "Intermission"
        }]
    }, {
        "resources": [{
            "type": "CourseActivity",
            "description": "Second section description",
            "title": "Second section title"
        }]
    }]
    course = models.Course(sections=json.dumps(data))
    sections, activities = course.moodle_activities()

    assert sections == [
        {'id': 1, 'sequence': [1, 2]},
        {'id': 2, 'sequence': [3]},
    ]

    assert activities == [
        {'id': 1, 'type': 'page', 'intro': 'First slide', 'content': 'Hello world', 'section': 1},
        {'id': 2, 'type': 'page', 'intro': 'Intermission', 'content': 'Olé!', 'section': 1},
        {'id': 3, 'type': 'page', 'intro': 'Second section title', 'content': 'Second section description', 'section': 2},
    ]
