# -*- coding: utf-8 -*-

"""
Tests for ORB resource forms
"""

from mock import MagicMock
from django.conf import settings
from django.test import TestCase, override_settings


class ResourceStep2FormTests(TestCase):
    """Tests for the ResourceStep2Form form class"""

    @classmethod
    def setUpClass(cls):
        super(ResourceStep2FormTests, cls).setUpClass()
        cls.uploaded_file = MagicMock()
        cls.uploaded_file.content_type = "application/pdf"
        cls.uploaded_file.size = 100
        cls.uploaded_file._size = 100

    def test_valid_missing_url_file(self):
        """Form should be invalid when missing both file and URL"""
        from orb.forms import ResourceStep2Form
        form = ResourceStep2Form(data={"title": u"¡Olé!"})
        self.assertFalse(form.is_valid())

    def test_valid_url(self):
        """Form should be valid with only a URL

        Unicode is used for good measure to test encoding validation
        """
        from orb.forms import ResourceStep2Form
        form = ResourceStep2Form(data={
            "url": u"http://www.wvi.org/publication/manual-para-madres-gu%C3%ADas"})
        self.assertTrue(form.is_valid())

    def test_invalid_url(self):
        """Form shoudl reject invalid URLs"""
        from orb.forms import ResourceStep2Form
        form = ResourceStep2Form(data={"url": u"htp://example.com/olé"})
        self.assertFalse(form.is_valid())

    def test_valid_file(self):
        """Form should be valid with only a file"""
        from orb.forms import ResourceStep2Form
        form = ResourceStep2Form(files={"file": self.uploaded_file})
        self.assertTrue(form.is_valid())

    @override_settings(TASK_UPLOAD_FILE_MAX_SIZE=90)
    def test_file_exceeds_maxsize(self):
        """Form should be invalid if file size exceeds maxsize"""
        from orb.forms import ResourceStep2Form
        self.assertEqual(settings.TASK_UPLOAD_FILE_MAX_SIZE, 90)
        form = ResourceStep2Form(files={"file": self.uploaded_file})
        self.assertFalse(form.is_valid())

    @override_settings(TASK_UPLOAD_FILE_TYPE_BLACKLIST=['application/pdf'])
    def test_file_invalid_type(self):
        """Form should be invalid if file type is blacklisted"""
        from orb.forms import ResourceStep2Form
        form = ResourceStep2Form(files={"file": self.uploaded_file})
        self.assertFalse(form.is_valid())


class ReviewFormTests(TestCase):
    """
    Tests for the reviewer's review entry form
    """
    def test_accept_form(self):
        """Form should not require reason if resource approved"""
        from orb.resources.forms import ReviewForm
        form = ReviewForm(data={'approved': True})
        self.assertTrue(form.is_valid())

    def test_reject_no_reason(self):
        """Form should require reason if resource rejected"""
        from orb.resources.forms import ReviewForm
        form = ReviewForm(data={'approved': False})
        self.assertFalse(form.is_valid())
        form = ReviewForm(data={'approved': False, 'reason': ''})
        self.assertFalse(form.is_valid())

    def test_reject_with_reason(self):
        """Form should require reason if resource rejected"""
        from orb.resources.forms import ReviewForm
        form = ReviewForm(data={'approved': False, 'reason': u"¡Olé!"})
        self.assertTrue(form.is_valid())
