"""
An email based authentication backend.
"""

from __future__ import unicode_literals

import logging

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


class UserModelEmailBackend(ModelBackend):
    """Authenticate users by email address"""

    def authenticate(self, username="", password="", **kwargs):
        try:
            user = get_user_model().objects.get(email__iexact=username)
            if user.check_password(password):
                return user
            return None
        except get_user_model().DoesNotExist:
            return None
        except get_user_model().MultipleObjectsReturned:
            logging.exception("Multiple users returned for email auth using '{}'".format(username))
            return None
