"""
Tests for the courses app
"""

import pytest
from orb.tests.utils import request_factory

from orb.courses import views
from orb.courses import forms
from django.core.urlresolvers import reverse


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


def test_admin_can_edit_course():
    pass


def test_owner_can_edit_course():
    pass


def test_non_owner_cannot_edit_course():
    pass
