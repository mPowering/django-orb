# -*- coding: utf-8 -*-

import mock
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.http import Http404
from django.core.exceptions import PermissionDenied

from orb.resources.tests.factory import resource_factory
from orb.resources.views import review_resource
from orb.resources.models import ContentReview
from orb.models import UserProfile, Resource
from orb.tests.utils import request_factory, mocked_model


class ReviewViewTests(TestCase):

    @classmethod
    def setUpClass(cls):
        super(ReviewViewTests, cls).setUpClass()
        cls.reviewer = User.objects.create(username="reviewer")
        #reviewer_profile, _ = UserProfile.objects.get_or_create(user=cls.reviewer)
        cls.nonreviewer = User.objects.create(username="nonreviewer")
        #nonreviewer_profile, _  = UserProfile.objects.get_or_create(user=cls.reviewer)
        cls.resource = resource_factory(
            user=cls.reviewer,
            title=u"Básica salud del recién nacido",
            description=u"Básica salud del recién nacido",
        )
        cls.review = ContentReview.objects.create(resource=cls.resource, reviewer=cls.reviewer)

    @classmethod
    def tearDownClass(cls):
        super(ReviewViewTests, cls).tearDownClass()
        User.objects.all().delete()
        Resource.objects.all().delete()

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
