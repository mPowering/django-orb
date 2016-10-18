from django.test import TestCase
from django.contrib.auth import get_user_model
import mock
from orb.models import UserProfile, ReviewerRole


class ProfileReviewerTessts(TestCase):
    """Tests on class methods"""

    @classmethod
    def setUpClass(cls):
        super(ProfileReviewerTessts, cls).setUpClass()
        review_user = get_user_model().objects.create(username="zippy")
        cls.review_profile = UserProfile.objects.create(user=review_user)
        test_role = ReviewerRole.objects.create(name="reviewer")
        cls.review_profile.reviewer_roles.add(test_role)

        nonreview_user = get_user_model().objects.create(username="zappy")
        cls.nonreview_profile = UserProfile.objects.create(user=nonreview_user)

    def test_reviewer(self):
        self.assertTrue(self.review_profile.is_reviewer)
        self.assertFalse(self.nonreview_profile.is_reviewer)

    def test_reviewers(self):
        self.assertEqual(
            list(UserProfile.profiles.reviewers()),
            [self.review_profile],
        )

    def test_non_reviewers(self):
        self.assertEqual(
            list(UserProfile.profiles.nonreviewers()),
            [self.nonreview_profile],
        )
