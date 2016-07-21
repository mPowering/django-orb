# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse, resolve
from django.http import Http404
from django.test import TestCase

from orb.models import UserProfile, ReviewerRole
from orb.resources.models import ContentReview
from orb.resources.tests.factory import resource_factory
from orb.resources.views import review_resource, resource_review_list
from orb.tests.utils import request_factory, mocked_model


class ReviewBase(TestCase):
    """
    Sets up some common data for testing resource review related views
    """

    @classmethod
    def setUpClass(cls):
        super(ReviewBase, cls).setUpClass()
        cls.role, _ = ReviewerRole.objects.get_or_create(name='medical')
        cls.reviewer, _ = User.objects.get_or_create(username="reviewer")
        cls.nonreviewer, _ = User.objects.get_or_create(username="nonreviewer")
        cls.resource = resource_factory(
            user=cls.reviewer,
            title=u"Básica salud del recién nacido",
            description=u"Básica salud del recién nacido",
        )
        cls.review = ContentReview.objects.create(
            resource=cls.resource,
            reviewer=cls.reviewer,
            role=cls.role,
        )

    @classmethod
    def tearDownClass(cls):
        super(ReviewBase, cls).tearDownClass()
        User.objects.all().delete()


class ReviewViewTests(ReviewBase):

    def test_url(self):
        reverse("orb_resource_review",
                kwargs={'resource_id': 123, 'review_id': 123})

    def test_anonymous_user(self):
        """Anon users should not be permitted to view this"""
        request = request_factory()
        response = review_resource(request, 123, 123)
        self.assertEqual(response.status_code, 302)

    def test_missing_review(self):
        """A 404 should be raised for a reviewer if Resource is missing"""
        mock_profile = mocked_model(UserProfile)
        mock_profile.is_reviewer = True
        request = request_factory(user=self.reviewer, userprofile=mock_profile)
        self.assertRaises(
            Http404,
            review_resource,
            request,
            123,
            123,
        )

    def test_unassigned_content_reviewer(self):
        """An unassigned content review should not be able to access the view"""
        mock_profile = mocked_model(UserProfile)
        mock_profile.is_reviewer = True
        request = request_factory(user=self.nonreviewer, userprofile=mock_profile)
        self.assertRaises(
            PermissionDenied,
            review_resource,
            request,
            self.resource.pk,
            self.review.pk,
        )

    def test_assigned_content_review(self):
        """The assigned content review should be able to access the view"""
        mock_profile = mocked_model(UserProfile)
        mock_profile.is_reviewer = True
        request = request_factory(user=self.reviewer, userprofile=mock_profile)
        response = review_resource(request, self.resource.pk, self.review.pk)
        self.assertEqual(response.status_code, 200)


class ReviewListTests(ReviewBase):

    def test_url(self):
        url = reverse("orb_pending_resources")
        resolution = resolve(url)
        self.assertEqual(resolution.func, resource_review_list)

    def test_anon_users_only(self):
        """Anon users should be redirected"""
        request = request_factory()
        response = resource_review_list(request)
        self.assertEqual(response.status_code, 302)

    def test_regular_users(self):
        """Non-reviewers should not be permitted"""
        mock_profile = mocked_model(UserProfile)
        mock_profile.is_reviewer = False
        request = request_factory(user=self.nonreviewer, userprofile=mock_profile)
        self.assertRaises(
            PermissionDenied,
            resource_review_list,
            request,
        )

    def test_reviewer_users(self):
        """Reviewer users should be able to see the page"""
        mock_profile = mocked_model(UserProfile)
        mock_profile.is_reviewer = True
        request = request_factory(user=self.reviewer, userprofile=mock_profile)
        response = resource_review_list(request)
        self.assertEqual(response.status_code, 200)
