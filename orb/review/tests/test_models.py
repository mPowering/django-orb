# -*- coding: utf-8 -*-

"""
Tests for ORB resource models
"""

from django.contrib.auth.models import User
from django.test import TestCase

from orb.models import Resource, ReviewerRole
from orb.resources.tests.factory import resource_factory
from orb.review.models import ContentReview, process_resource_reviews


class ResourceStatusTests(TestCase):
    """
    Tests for processing a change in a review
    """

    @classmethod
    def setUpClass(cls):
        super(ResourceStatusTests, cls).setUpClass()
        cls.user = User.objects.create(username="tester")
        cls.other_user = User.objects.create(username="milton")
        cls.resource = resource_factory(
            user=cls.user,
            title=u"Básica salud del recién nacido",
            description=u"Básica salud del recién nacido",
        )
        cls.medical = ReviewerRole.objects.create(name='medical')
        cls.technical = ReviewerRole.objects.create(name='technical')

    @classmethod
    def tearDownClass(cls):
        super(ResourceStatusTests, cls).tearDownClass()
        User.objects.all().delete()
        Resource.objects.all().delete()

    def test_all_approved(self):
        """Resource should be approved when all reviews are approved"""
        ContentReview.objects.create(role=self.medical, reviewer=self.user,
                                     resource=self.resource, status='approved')
        ContentReview.objects.create(role=self.technical, reviewer=self.other_user,
                                     resource=self.resource, status='approved')
        self.resource.status = Resource.PENDING
        result = process_resource_reviews(self.resource)
        self.assertEqual(result, Resource.APPROVED)

    def test_any_rejected(self):
        """Resource should be rejected if any review is rejected"""
        ContentReview.objects.create(role=self.medical, reviewer=self.user,
                                     resource=self.resource, status='approved')
        ContentReview.objects.create(role=self.technical, reviewer=self.other_user,
                                     resource=self.resource, status='rejected')
        self.resource.status = Resource.PENDING
        result = process_resource_reviews(self.resource)
        self.assertEqual(result, Resource.REJECTED)

    def test_incomplete_rejection(self):
        """Should not change status on rejection if reviews incomplete"""
        ContentReview.objects.create(role=self.technical, reviewer=self.other_user,
                                     resource=self.resource, status='rejected')
        self.resource.status = Resource.PENDING
        result = process_resource_reviews(self.resource)
        self.assertEqual(result, Resource.PENDING)

    def test_incomplete_approval(self):
        """Should not change status on approval if reviews incomplete"""
        ContentReview.objects.create(role=self.technical, reviewer=self.other_user,
                                     resource=self.resource, status='approved')
        self.resource.status = Resource.PENDING
        result = process_resource_reviews(self.resource)
        self.assertEqual(result, Resource.PENDING)
