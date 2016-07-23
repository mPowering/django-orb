# -*- coding: utf-8 -*-

"""
Tests for ORB resource models
"""

from django.contrib.auth.models import User
from django.test import TestCase

from orb.models import Resource, ResourceURL, ReviewerRole
from orb.resources.models import ContentReview, process_resource_reviews
from orb.resources.tests.factory import resource_factory


class ResourceTests(TestCase):
    """Basic tests of the Resource model and its methods"""

    @classmethod
    def setUpClass(cls):
        super(ResourceTests, cls).setUpClass()
        cls.user = User.objects.create(username="tester")
        cls.resource = resource_factory(
            user=cls.user,
            title=u"Básica salud del recién nacido",
            description=u"Básica salud del recién nacido",
        )

    @classmethod
    def tearDownClass(cls):
        super(ResourceTests, cls).tearDownClass()
        User.objects.all().delete()
        Resource.objects.all().delete()

    def test_absolute_url(self):
        """URL is returned with slug"""
        self.assertEqual(
            self.resource.get_absolute_url(),
            "/resource/view/basica-salud-del-recien-nacido"
        )

    def test_unicode_display(self):
        """Unicode value of title is returned"""
        self.assertEqual(
            self.resource.__unicode__(),
            u"Básica salud del recién nacido",
        )

    def test_unique_slugification(self):
        """Unique slug is generated for new resources"""
        duplicate = resource_factory(
            user=self.user,
            title=u"Básica salud del recién nacido",
            description=u"Básica salud del recién nacido",
        )
        self.assertEqual(
            self.resource.slug,
            "basica-salud-del-recien-nacido"
        )
        self.assertEqual(
            duplicate.slug,
            "basica-salud-del-recien-nacido-2"
        )

    def test_non_latin_slugification(self):
        """Non-latin characters should be transliterated"""
        cyrillic_resource= resource_factory(
            user=self.user,
            title=u"Санкт-Петербург Питоны",  # Saint Petersburg Pythons
            description=u"Some resource",
        )
        self.assertEqual(cyrillic_resource.slug, u"sankt-peterburg-pitony")

        chinese_resource= resource_factory(
            user=self.user,
            title=u"北京蟒蛇",  # Beijing Pythons
            description=u"Some resource",
        )
        self.assertEqual(chinese_resource.slug, u"bei-jing-mang-she")


class ResourceURLTests(TestCase):
    """Basic tests of the ResourceURL model and its methods"""

    @classmethod
    def setUpClass(cls):
        super(ResourceURLTests, cls).setUpClass()
        cls.user = User.objects.create(username="tester")
        cls.resource = resource_factory(
            user=cls.user,
            title=u"Básica salud del recién nacido",
            description=u"Básica salud del recién nacido",
        )
        cls.resource_url = ResourceURL.objects.create(
            resource=cls.resource,
            url=u"http://www.example.com/niños",
            create_user=cls.user,
            update_user=cls.user,
        )

    @classmethod
    def tearDownClass(cls):
        super(ResourceURLTests, cls).tearDownClass()
        User.objects.all().delete()
        Resource.objects.all().delete()

    def test_unicode_display(self):
        """Unicode value of URL is returned"""
        self.assertEqual(
            self.resource_url.__unicode__(),
            u"http://www.example.com/niños",
        )


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
