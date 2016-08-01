# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.test import TestCase

from orb.models import ReviewerRole, UserProfile
from orb.resources.tests.factory import resource_factory
from orb.review.models import ContentReview


class ReviewBase(TestCase):
    """
    Base class for setting up common data for testing resource review related views
    """

    @classmethod
    def setUpClass(cls):
        super(ReviewBase, cls).setUpClass()

        cls.medical_role, _ = ReviewerRole.objects.get_or_create(name='medical')
        cls.technical_role, _ = ReviewerRole.objects.get_or_create(name='technical')

        cls.staff_user, _ = User.objects.get_or_create(username="staff", is_staff=True)
        cls.reviewer, _ = User.objects.get_or_create(username="reviewer")
        cls.nonreviewer, _ = User.objects.get_or_create(username="nonreviewer")

        cls.profile_one, _ = UserProfile.objects.get_or_create(
            user=cls.staff_user,
            reviewer_role=cls.medical_role,
        )
        cls.profile_two, _ = UserProfile.objects.get_or_create(
            user=cls.reviewer,
            reviewer_role=cls.technical_role,
        )

        cls.resource = resource_factory(
            user=cls.reviewer,
            title=u"Básica salud del recién nacido",
            description=u"Básica salud del recién nacido",
        )

    @classmethod
    def tearDownClass(cls):
        super(ReviewBase, cls).tearDownClass()
        User.objects.all().delete()