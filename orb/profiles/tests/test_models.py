from django.test import TestCase
import mock
from orb.models import UserProfile, ReviewerRole


class ProfileMethodTests(TestCase):
    """Tests on class methods"""

    def test_reviewer(self):
        model_state = mock.Mock()
        model_state.db = 'default'
        mocked_role = mock.Mock(spec=ReviewerRole)
        mocked_role._state = model_state
        profile = UserProfile(reviewer_role=mocked_role)

        self.assertTrue(profile.is_reviewer)

        self.assertFalse(UserProfile().is_reviewer)
