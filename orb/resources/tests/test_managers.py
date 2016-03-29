# -*- coding: utf-8 -*-

"""
Tests for ORB resource models
"""

from django.contrib.auth.models import User, AnonymousUser
from django.test import TestCase

from orb.models import Resource
from orb.resources.tests.factory import resource_factory


class ResourceTests(TestCase):
    """Basic tests of the Resource model and its methods"""

    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create(username="tester")
        cls.staff = User.objects.create(username="staff", is_staff=True)

        cls.resource = resource_factory(
            user=cls.user,
            title=u"Básica salud del recién nacido",
            description=u"Básica salud del recién nacido",
            status=Resource.APPROVED,
        )
        cls.resource = resource_factory(
            user=cls.user,
            title=u"Unapproved resource",
            description=u"Unapproved, owned by user",
        )
        cls.resource = resource_factory(
            user=cls.staff,
            title=u"Staff resource",
            description=u"Unapproved, owned by staff user",
        )

    @classmethod
    def tearDownClass(cls):
        User.objects.all().delete()
        Resource.objects.all().delete()


    def test_default_manager(self):
        """Sanity check on defaults"""
        self.assertEqual(Resource.objects.all().count(), 3)

    def test_approved(self):
        self.assertEqual(Resource.objects.approved().count(), 1)

    def test_approved_anon(self):
        """Should be equal to default approved count"""
        self.assertEqual(Resource.objects.approved(user=AnonymousUser).count(), 1)

    def test_approved_owner(self):
        """Should include resources created by user"""
        self.assertEqual(Resource.objects.approved(user=self.user).count(), 2)

    def test_approved_staff(self):
        """Should include all resources regardless of status"""
        self.assertEqual(Resource.objects.approved(user=self.staff).count(), 3)
