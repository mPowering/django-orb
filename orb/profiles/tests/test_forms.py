"""Tests for profile/registration forms"""

from __future__ import unicode_literals

import pytest
import unittest2 as unittest
from faker import Faker
from hypothesis import given
from hypothesis import strategies as st

from orb.profiles import forms


@pytest.mark.django_db
class TestRegisterForm(unittest.TestCase):

    def setUp(self):
        super(TestRegisterForm, self).setUp()
        fake = Faker()
        self.profile_info = fake.profile()
        self.form_class = forms.RegisterForm

    @given(
        st.booleans(),
        st.text(max_size=20),  # password
        st.booleans(),  # use_password
        st.text(max_size=20),  # confirm password
        st.booleans(),  # use_confirm_password
        st.booleans(),  # match_confirm_password
        st.text(max_size=20),  # first_name
        st.booleans(),  # use_first_name
        st.text(max_size=20),  # last_name
        st.booleans(),  # use_last_name
        st.text(max_size=200),  # organisation
        st.booleans(),  # use_organisation
        st.booleans(),  # terms

    )
    def test_form_validity(self, use_email, password, use_password, confirm_password, use_confirm_password,
                           match_confirm_password, first_name, use_first_name, last_name, use_last_name,
                           organisation, use_organisiation, terms):
        """
        Ensure form is valid with required fields

        Tests with REQUIRED fields only
        """

        email = self.profile_info['mail'] if use_email else ''
        password = password if use_password else ''
        confirm_password = '' if not use_confirm_password else (password if match_confirm_password else confirm_password)
        first_name = first_name if use_first_name else ''
        last_name = last_name if use_last_name else ''
        organisation = organisation if use_organisiation else ''

        data = {
            'email': email,
            'password': password,
            'password_again': confirm_password,
            'first_name': first_name,
            'last_name': last_name,
            'terms': terms,
            'organisation': organisation,
        }
        form = self.form_class(data=data)

        form_validity = True

        if any([
            not email,
                len(password) < 6,
                password != confirm_password,
                len(first_name) < 2,
                len(first_name) > 100,
                len(last_name) < 2,
                len(last_name) > 100,
                len(organisation) < 1,
                len(organisation) > 100,
            not terms,

        ]):
            form_validity = False

        form_valid = form.is_valid()

        if form_validity != form_valid:
            if form_valid:
                print(data)
            else:
                print(form.errors)

        self.assertEqual(form.is_valid(), form_validity)


@pytest.mark.django_db
class TestProfileForm(unittest.TestCase):

    def setUp(self):
        super(TestProfileForm, self).setUp()
        fake = Faker()
        self.profile_info = fake.profile()
        self.form_class = forms.ProfileForm

    @given(
        st.booleans(),
        st.text(max_size=200),  # password
        st.booleans(),  # use_password
        st.text(max_size=200),  # confirm password
        st.booleans(),  # use_confirm_password
        st.booleans(),  # match_confirm_password
        st.text(max_size=200),  # first_name
        st.booleans(),  # use_first_name
        st.text(max_size=200),  # last_name
        st.booleans(),  # use_last_name
        st.text(max_size=200),  # organisation
        st.booleans(),  # use_organisation
    )
    def test_form_validity(self, use_email, password, use_password, confirm_password, use_confirm_password,
                           match_confirm_password, first_name, use_first_name, last_name, use_last_name,
                           organisation, use_organisiation):
        """
        Ensure form is valid with required fields

        Tests with REQUIRED fields only
        """
        email = self.profile_info['mail'] if use_email else ''
        password = password if use_password else ''
        confirm_password = '' if not use_confirm_password else (password if match_confirm_password else confirm_password)
        first_name = first_name if use_first_name else ''
        last_name = last_name if use_last_name else ''
        organisation = organisation if use_organisiation else ''

        data={
            'email': email,
            'password': password,
            'password_again': confirm_password,
            'first_name': first_name,
            'last_name': last_name,
            'organisation': organisation,
        }
        form = self.form_class(data=data)

        form_validity = True

        if any([
            not email,
            password and len(password) < 6,
            password != confirm_password,
            len(first_name) < 2,
            len(first_name) > 100,
            len(last_name) < 2,
            len(last_name) > 100,
            len(organisation) < 1,
            len(organisation) > 100,
        ]):
            form_validity = False

        form_valid = form.is_valid()

        if form_validity != form_valid:
            if form_valid:
                print(data)
            else:
                print(form.errors)

        self.assertEqual(form.is_valid(), form_validity)
