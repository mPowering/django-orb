from django.test import TestCase
from orb.models import UserProfile


class ProfileMethodTests(TestCase):
    """Tests on class methods"""

    def test_reviewer(self):
        self.assertTrue(UserProfile(crt_member=True).is_reviewer)
        self.assertTrue(UserProfile(mep_member=True).is_reviewer)
        self.assertTrue(UserProfile(mep_member=True, crt_member=True).is_reviewer)
        self.assertFalse(UserProfile().is_reviewer)
