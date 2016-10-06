from django.test import TestCase
from django.contrib.auth import get_user_model
import mock
from orb.models import UserProfile, ReviewerRole


class ProfileMethodTests(TestCase):
    """Tests on class methods"""

    def test_reviewer(self):

        review_user = get_user_model().objects.create(username="zippy")
        review_profile = UserProfile.objects.create(user=review_user)
        test_role = ReviewerRole.objects.create(name="reviewer")
        review_profile.reviewer_roles.add(test_role)

        nonreview_user = get_user_model().objects.create(username="zappy")
        nonreview_profile = UserProfile.objects.create(user=nonreview_user)

        self.assertTrue(review_profile.is_reviewer)

        self.assertFalse(nonreview_profile.is_reviewer)


