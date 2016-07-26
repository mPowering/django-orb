# -*- coding: utf-8 -*-

"""
Tests for ORB resource forms
"""

from django.test import TestCase


class ReviewFormTests(TestCase):
    """
    Tests for the reviewer's review entry form
    """
    def test_accept_form(self):
        """Form should not require reason if resource approved"""
        from orb.review.forms import ReviewForm
        form = ReviewForm(data={'approved': True})
        self.assertTrue(form.is_valid())

    def test_reject_no_reason(self):
        """Form should require reason if resource rejected"""
        from orb.review.forms import ReviewForm
        form = ReviewForm(data={'approved': False})
        self.assertFalse(form.is_valid())
        form = ReviewForm(data={'approved': False, 'reason': ''})
        self.assertFalse(form.is_valid())

    def test_reject_with_reason(self):
        """Form should require reason if resource rejected"""
        from orb.review.forms import ReviewForm
        form = ReviewForm(data={'approved': False, 'reason': u"¡Olé!"})
        self.assertTrue(form.is_valid())
