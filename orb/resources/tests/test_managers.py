# -*- coding: utf-8 -*-

"""
Tests for ORB resource models
"""

from django.contrib.auth.models import User, AnonymousUser
from django.test import TestCase

from orb.models import Resource, ResourceURL, UserProfile
from orb.resources.tests.factory import resource_factory, resource_url_factory


class ResourceTests(TestCase):
    """Tests for the managers associated with the Resource model.

    Tests are consolidated because the returned ApprovedManager queryset should
    be the same as the queryset for the ResourceManager.approved method. Same
    data same tests.
    """

    @classmethod
    def setUpClass(cls):
        super(ResourceTests, cls).setUpClass()
        cls.user = User.objects.create(username="tester")
        cls.updater = User.objects.create(username="updater")
        cls.staff = User.objects.create(username="staff", is_staff=True)
        cls.mep_user = User.objects.create(username="mep")
        UserProfile.objects.create(user=cls.mep_user, mep_member=True)
        cls.crt_user = User.objects.create(username="crt")
        UserProfile.objects.create(user=cls.crt_user, crt_member=True)

        approved = resource_factory(
            user=cls.user,
            title=u"Básica salud del recién nacido",
            description=u"Básica salud del recién nacido",
            status=Resource.APPROVED,
        )
        unapproved_user = resource_factory(
            create_user=cls.user,
            update_user=cls.updater,
            title=u"Unapproved resource",
            description=u"Unapproved, owned by user",
        )
        unapproved_staff = resource_factory(
            user=cls.staff,
            title=u"Staff resource",
            description=u"Unapproved, owned by staff user",
        )

        resource_url_factory(resource=approved, user=cls.user)
        resource_url_factory(resource=unapproved_user, user=cls.user)


    @classmethod
    def tearDownClass(cls):
        super(ResourceTests, cls).tearDownClass()
        User.objects.all().delete()
        Resource.objects.all().delete()

    # Tests for the ResourceManager

    def test_default_manager(self):
        """Sanity check on defaults"""
        self.assertEqual(Resource.objects.all().count(), 3)

    def test_approved(self):
        self.assertEqual(Resource.objects.approved().count(), 1)

    def test_approved_anon(self):
        """Should be equal to default approved count"""
        self.assertEqual(Resource.objects.approved(user=AnonymousUser()).count(), 1)

    def test_approved_creator(self):
        """Should include resources created by user"""
        self.assertEqual(Resource.objects.approved(user=self.user).count(), 2)

    def test_approved_updater(self):
        """Should include resources updated by user"""
        self.assertEqual(Resource.objects.approved(user=self.updater).count(), 2)

    def test_approved_staff(self):
        """Staff should include all resources regardless of status"""
        self.assertEqual(Resource.objects.approved(user=self.staff).count(), 3)

    def test_approved_mep_reviewer(self):
        """Reviewer should include all resources regardless of status"""
        self.assertEqual(Resource.objects.approved(user=self.mep_user).count(), 3)

    def test_approved_crt_reviewer(self):
        """Reviewer should include all resources regardless of status"""
        self.assertEqual(Resource.objects.approved(user=self.crt_user).count(), 3)

    # Tests for the ApprovalManager

    def test_approval_manager(self):
        self.assertEqual(Resource.approved.all().count(), 1)

    def test_approved_anon(self):
        """Should be equal to default approved count"""
        self.assertEqual(Resource.approved.filter(user=AnonymousUser()).count(), 1)

    def test_approved_owner(self):
        """Should include resources created by user"""
        self.assertEqual(Resource.approved.filter(user=self.user).count(), 2)

    def test_approved_staff(self):
        """Should include all resources regardless of status"""
        self.assertEqual(Resource.approved.filter(user=self.staff).count(), 3)

    def test_get_approved(self):
        assert Resource.approved.get(user=self.user, title=u"Unapproved resource")

    # Tests for ResourceURL

    def test_approved_urls(self):
        """Only one resource URL should be returned for anon user"""
        self.assertEqual(ResourceURL.objects.approved(user=AnonymousUser()).count(), 1)

    def test_staff_urls(self):
        """All ResourceURLs should be returned for staff user"""
        self.assertEqual(ResourceURL.objects.approved(user=self.staff).count(), 2)
