# -*- coding: utf-8 -*-

"""
Tests for ORB resource models
"""

from django.contrib.auth.models import User
from django.test import TestCase
from django_fsm import TransitionNotAllowed
from django.core import mail

from orb.models import Resource, ReviewerRole
from orb.resources.tests.factory import resource_factory
from orb.review.models import ContentReview, process_resource_reviews


class ReviewBase(TestCase):

    @classmethod
    def setUpClass(cls):
        super(ReviewBase, cls).setUpClass()
        cls.user = User.objects.create(username="tester", email="tester@acme.org")
        cls.other_user = User.objects.create(username="milton", email="milton@acme.org")
        cls.resource = resource_factory(
            user=cls.user,
            title=u"Básica salud del recién nacido",
            description=u"Básica salud del recién nacido",
        )
        cls.medical = ReviewerRole.objects.create(name='medical')
        cls.technical = ReviewerRole.objects.create(name='technical')

    @classmethod
    def tearDownClass(cls):
        super(ReviewBase, cls).tearDownClass()
        User.objects.all().delete()
        ReviewerRole.objects.all().delete()
        Resource.objects.all().delete()


class ProcessReviewsTests(ReviewBase):
    """
    Tests for processing a change in a review
    """

    def test_process_all_approved(self):
        """Resource should be approved when all reviews are approved"""
        ContentReview.objects.create(role=self.medical, reviewer=self.user,
                                     resource=self.resource, status='approved')
        ContentReview.objects.create(role=self.technical, reviewer=self.other_user,
                                     resource=self.resource, status='approved')
        self.resource.status = Resource.PENDING
        result = process_resource_reviews(self.resource)
        self.assertEqual(result, Resource.APPROVED)

    def test_process_any_rejected(self):
        """Resource should be rejected if any review is rejected"""
        ContentReview.objects.create(role=self.medical, reviewer=self.user,
                                     resource=self.resource, status='approved')
        ContentReview.objects.create(role=self.technical, reviewer=self.other_user,
                                     resource=self.resource, status='rejected')
        self.resource.status = Resource.PENDING
        result = process_resource_reviews(self.resource)
        self.assertEqual(result, Resource.REJECTED)

    def test_process_incomplete_rejection(self):
        """Should not change status on rejection if reviews incomplete"""
        ContentReview.objects.create(role=self.technical, reviewer=self.other_user,
                                     resource=self.resource, status='rejected')
        self.resource.status = Resource.PENDING
        result = process_resource_reviews(self.resource)
        self.assertEqual(result, Resource.PENDING)

    def test_process_incomplete_approval(self):
        """Should not change status on approval if reviews incomplete"""
        ContentReview.objects.create(role=self.technical, reviewer=self.other_user,
                                     resource=self.resource, status='approved')
        self.resource.status = Resource.PENDING
        result = process_resource_reviews(self.resource)
        self.assertEqual(result, Resource.PENDING)


class AssignmentTests(ReviewBase):
    """
    Test assignment functionality
    """

    def test_new_assignment_email(self):
        """Assigned review should get an assignment email"""
        ContentReview.reviews.all().delete()
        inbox_count = len(mail.outbox)
        review = ContentReview.reviews.assign(
            role=self.medical,
            reviewer=self.other_user,
            resource=self.resource, status='approved',
        )
        self.assertEqual(inbox_count + 1, len(mail.outbox))

    def test_reassign_self(self):
        """Reassignment to self should do nothing"""
        review = ContentReview.objects.create(
            role=self.technical,
            reviewer=self.other_user,
            resource=self.resource,
        )
        self.assertIsNone(review.reassign(self.other_user))

    def test_reassign_completed(self):
        review = ContentReview.objects.create(
            role=self.technical,
            reviewer=self.other_user,
            resource=self.resource,
            status='approved',
        )
        self.assertRaises(
            TransitionNotAllowed,
            review.reassign,
            self.user,
        )


class ReviewIntegrationTests(ReviewBase):
    """
    Tests that when the last review is finally rejected or approved, the
    resource status changes and emails sent out as necessary
    """