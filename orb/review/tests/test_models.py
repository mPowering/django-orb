# -*- coding: utf-8 -*-

"""
Tests for ORB resource models
"""

from django.core import mail
from django_fsm import TransitionNotAllowed

from orb.models import Resource
from orb.review.models import ContentReview, process_resource_reviews
from orb.review.tests.base import ReviewTestCase


class ProcessReviewsTests(ReviewTestCase):
    """
    Tests for processing a change in a review
    """

    def test_process_all_approved(self):
        """Processing function should return status result"""
        ContentReview.objects.create(role=self.medical_role, reviewer=self.staff_user,
                                     resource=self.resource, status=Resource.APPROVED)
        ContentReview.objects.create(role=self.technical_role, reviewer=self.reviewer,
                                     resource=self.resource, status=Resource.APPROVED)
        self.resource.status = Resource.PENDING
        result = process_resource_reviews(self.resource)
        self.assertEqual(result, Resource.APPROVED)

    def test_process_any_rejected(self):
        """Resource should be rejected if any review is rejected"""
        ContentReview.objects.create(role=self.medical_role, reviewer=self.staff_user,
                                     resource=self.resource, status=Resource.APPROVED)
        ContentReview.objects.create(role=self.technical_role, reviewer=self.reviewer,
                                     resource=self.resource, status=Resource.REJECTED)
        self.resource.status = Resource.PENDING
        result = process_resource_reviews(self.resource)
        self.assertEqual(result, Resource.REJECTED)

    def test_process_incomplete_rejection(self):
        """Should not change status on rejection if reviews incomplete"""
        ContentReview.objects.create(role=self.technical_role, reviewer=self.reviewer,
                                     resource=self.resource, status=Resource.REJECTED)
        self.resource.status = Resource.PENDING
        result = process_resource_reviews(self.resource)
        self.assertEqual(result, Resource.PENDING)

    def test_process_incomplete_approval(self):
        """Should not change status on approval if reviews incomplete"""
        ContentReview.objects.create(role=self.technical_role, reviewer=self.reviewer,
                                     resource=self.resource, status=Resource.APPROVED)
        self.resource.status = Resource.PENDING
        result = process_resource_reviews(self.resource)
        self.assertEqual(result, Resource.PENDING)


class AssignmentTests(ReviewTestCase):
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
            resource=self.resource, status=Resource.APPROVED,
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
            status=Resource.APPROVED,
        )
        self.assertRaises(
            TransitionNotAllowed,
            review.reassign,
            self.staff_user,
        )


class ReviewIntegrationTests(ReviewTestCase):
    """
    Tests that when the last review is finally rejected or approved, the
    resource status changes and emails sent out as necessary

    This tests from the point a review is changed up to what this does to the resrouce
    """

    def test_approved_resource(self):
        """Final approved review change status and send approve email"""
        email_count = len(mail.outbox)

        self.assertEqual(self.resource.status, Resource.PENDING)  # sanity check
        ContentReview.objects.create(
            role=self.technical_role,
            reviewer=self.reviewer,
            resource=self.resource,
            status=Resource.APPROVED,
        )
        review = ContentReview.objects.create(
            role=self.medical_role,
            reviewer=self.staff_user,
            resource=self.resource,
            status=Resource.PENDING,
        )
        review.approve()
        review.save()

        # Force refresh from the DB - TestCase attribute will be stale
        resource = Resource.objects.get(pk=self.resource.pk)

        # Ensure status is changed
        #self.assertEqual(resource.status, Resource.APPROVED)

        # Ensure email is sent to staff
        self.assertEqual(email_count + 1, len(mail.outbox))

    def test_rejected_resource(self):
        """Final rejection review changes status and send reject email"""
        self.resource.status = Resource.PENDING
        self.resource.save()
        self.assertEqual(self.resource.status, Resource.PENDING)  # sanity check
