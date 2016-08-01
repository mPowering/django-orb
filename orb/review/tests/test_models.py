# -*- coding: utf-8 -*-

"""
Tests for ORB resource models
"""

from django.core import mail
from django_fsm import TransitionNotAllowed

from orb.models import Resource
from orb.review.models import ContentReview, process_resource_reviews
from orb.review.tests.base import ReviewBase


class ProcessReviewsTests(ReviewBase):
    """
    Tests for processing a change in a review
    """

    def test_process_all_approved(self):
        """Resource should be approved when all reviews are approved"""
        ContentReview.objects.create(role=self.medical_role, reviewer=self.staff_user,
                                     resource=self.resource, status='approved')
        ContentReview.objects.create(role=self.technical_role, reviewer=self.reviewer,
                                     resource=self.resource, status='approved')
        self.resource.status = Resource.PENDING
        result = process_resource_reviews(self.resource)
        self.assertEqual(result, Resource.APPROVED)

    def test_process_any_rejected(self):
        """Resource should be rejected if any review is rejected"""
        ContentReview.objects.create(role=self.medical_role, reviewer=self.staff_user,
                                     resource=self.resource, status='approved')
        ContentReview.objects.create(role=self.technical_role, reviewer=self.reviewer,
                                     resource=self.resource, status='rejected')
        self.resource.status = Resource.PENDING
        result = process_resource_reviews(self.resource)
        self.assertEqual(result, Resource.REJECTED)

    def test_process_incomplete_rejection(self):
        """Should not change status on rejection if reviews incomplete"""
        ContentReview.objects.create(role=self.technical_role, reviewer=self.reviewer,
                                     resource=self.resource, status='rejected')
        self.resource.status = Resource.PENDING
        result = process_resource_reviews(self.resource)
        self.assertEqual(result, Resource.PENDING)

    def test_process_incomplete_approval(self):
        """Should not change status on approval if reviews incomplete"""
        ContentReview.objects.create(role=self.technical_role, reviewer=self.reviewer,
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
            role=self.medical_role,
            reviewer=self.staff_user,
            resource=self.resource, status='approved',
        )
        self.assertEqual(inbox_count + 1, len(mail.outbox))

    def test_reassign_self(self):
        """Reassignment to self should do nothing"""
        review = ContentReview.objects.create(
            role=self.technical_role,
            reviewer=self.reviewer,
            resource=self.resource,
        )
        self.assertIsNone(review.reassign(self.reviewer))

    def test_reassign_completed(self):
        review = ContentReview.objects.create(
            role=self.technical_role,
            reviewer=self.reviewer,
            resource=self.resource,
            status='approved',
        )
        self.assertRaises(
            TransitionNotAllowed,
            review.reassign,
            self.staff_user,
        )


class ReviewIntegrationTests(ReviewBase):
    """
    Tests that when the last review is finally rejected or approved, the
    resource status changes and emails sent out as necessary

    This tests from the point a review is changed up to what this does to the resrouce
    """

    def test_rejected_resource(self):
        """Final rejection review changes status and send reject email"""
        self.assertEqual(self.resource.status, Resource.PENDING)  # sanity check
        ContentReview.objects.create(
            role=self.technical_role,
            reviewer=self.reviewer,
            resource=self.resource,
            status='approved',
        )

    def test_approved_resource(self):
        """Final approved review change status and send approve email"""
        self.assertEqual(self.resource.status, Resource.PENDING)  # sanity check
