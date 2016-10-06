# -*- coding: utf-8 -*-

"""
Tests for ORB resource forms
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from orb.review.forms import ReviewForm
from orb.models import UserProfile, ReviewerRole

from orb.models import Resource
from orb.resources.tests.factory import resource_factory
from orb.review.forms import AssignmentForm
from orb.review.models import ContentReview


class ReviewFormTests(TestCase):
    """
    Tests for the reviewer's review entry form
    """
    def test_accept_form(self):
        """Form should not require reason if resource approved"""
        form = ReviewForm(data={'approved': True})
        self.assertTrue(form.is_valid())

    def test_reject_no_reason(self):
        """Form should require reason if resource rejected"""
        form = ReviewForm(data={'approved': False})
        self.assertFalse(form.is_valid())
        form = ReviewForm(data={'approved': False, 'reason': ''})
        self.assertFalse(form.is_valid())

    def test_reject_with_reason(self):
        """Form should require reason if resource rejected"""
        form = ReviewForm(data={'approved': False, 'reason': u"¡Olé!"})
        self.assertTrue(form.is_valid())


class AssignmentFormTests(TestCase):

    @classmethod
    def setUpClass(cls):
        super(AssignmentFormTests, cls).setUpClass()

        cls.user_one, _ = get_user_model().objects.get_or_create(username="one")
        cls.user_two, _ = get_user_model().objects.get_or_create(username="two")
        cls.user_three, _ = get_user_model().objects.get_or_create(username="three")
        cls.user_four, _ = get_user_model().objects.get_or_create(username="four")

        cls.medical_role, _ = ReviewerRole.objects.get_or_create(name='medical')
        cls.technical_role, _ = ReviewerRole.objects.get_or_create(name='technical')

        cls.profile_one, _ = UserProfile.objects.get_or_create(user=cls.user_one)
        cls.profile_one.reviewer_roles.add(cls.medical_role)

        cls.profile_two, _ = UserProfile.objects.get_or_create(user=cls.user_two)
        cls.profile_two.reviewer_roles.add(cls.technical_role)

        cls.profile_three, _ = UserProfile.objects.get_or_create(user=cls.user_three)
        cls.profile_three.reviewer_roles.add(cls.technical_role)

        cls.resource = resource_factory(
            user=cls.user_four,
            title=u"Básica salud del recién nacido",
            description=u"Básica salud del recién nacido",
        )

    @classmethod
    def tearDownClass(cls):
        super(AssignmentFormTests, cls).tearDownClass()
        get_user_model().objects.all().delete()
        ReviewerRole.objects.all().delete()
        ContentReview.objects.all().delete()

    def test_field_count(self):
        """If no assignments, should have no initial values"""
        form = AssignmentForm(resource=self.resource)
        self.assertEqual(2, len(form.fields))

    def test_initial_values(self):
        """If no assignments, should have no initial values"""
        form = AssignmentForm(resource=self.resource)
        for value in form.initial.itervalues():
            self.assertEqual(value, None)

    def test_has_assignments(self):
        """If assignments, should have initial values"""
        review = ContentReview.reviews.create(
            resource=self.resource,
            reviewer=self.user_one,
            role=self.medical_role,
        )

        form = AssignmentForm(resource=self.resource)
        self.assertEqual(
            {"technical": None, "medical": self.profile_one},
            form.initial,
        )
        ContentReview.reviews.all().delete()

    def test_review_completed(self):
        """Field should not be changable if review completed"""
        ContentReview.reviews.create(
            resource=self.resource,
            reviewer=self.user_two,
            role=self.technical_role,
            status=Resource.APPROVED,
        )

        form = AssignmentForm(resource=self.resource, data={
            'technical': self.profile_three.pk,
        })
        self.assertFalse(form.is_valid())
        ContentReview.reviews.all().delete()

    def test_save_reviews(self):
        """Save should create new assignments"""
        count = ContentReview.reviews.all().count()
        form = AssignmentForm(resource=self.resource, data={
            'medical': self.profile_one.pk,
        })
        self.assertTrue(form.is_valid())
        form.save()
        self.assertEqual(count + 1, ContentReview.reviews.all().count())
        ContentReview.reviews.all().delete()
