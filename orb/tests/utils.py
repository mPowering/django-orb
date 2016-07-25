"""
Utility functions for enhancing the reusability and readability of test code
"""

from functools import wraps

import mock
from django.conf import settings
from django.contrib.auth import SESSION_KEY
from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory
from django.utils.importlib import import_module


def request_factory(factory=None, user=None, userprofile=None, method='GET', **kwargs):
    """A function that returns a request object configured with a user (either
    a provided user or an anonymous user) as well as a session attribute.
    Useful anywhere testing against user state of any kind is required in a
    view.

    Based on this gist: https://gist.github.com/964472
    """
    if factory is None:
        factory = RequestFactory()
    engine = import_module(settings.SESSION_ENGINE)
    request = factory.request(REQUEST_METHOD=method)
    request.session = engine.SessionStore()
    request.session[SESSION_KEY] = getattr(user, 'id', 12)
    request.features = kwargs.get('features', {})
    request.user = user or AnonymousUser()
    if userprofile:
        request.user.userprofile = userprofile
    for key in kwargs:
        setattr(request, "{0}".format(key), kwargs[key])
    return request


def mocked_model(spec_model):
    """
    Returns a Mock that can be used like a related object

    >>> some_mock = mocked_model(MyRelatedModel)
    >>> some_mock.foo = True
    >>> resource = Resource.objects.create(..)
    >>> resource.bar = some_mock

    Without doing this, you'll get errors like:

    ValueError: Cannot assign "<MagicMock id='4554528976'>":
            "User.userprofile" must be a "UserProfile" instance.

    Args:
        spec_model: a model class

    Returns:
        Mock

    """
    model_state = mock.MagicMock()
    model_state.db = 'default'

    mock_profile = mock.MagicMock(spec=spec_model)
    mock_profile._state = model_state
    return mock_profile


def login_client(username, password):
    """
    A decorator for test methods that logs in a user and logs out for
    the duration of the test method. Should be used on TestCase test
    methods.

        class SomeTests(TestCase):

            @login_client(username="bob", password="pass")
            def test_api(self):
                self.assertEqual(
                        self.client.get("/admin/").status_code,
                        200,
                )

    Ought to be a context manager, too!
    """
    def decorator(test_method):
        @wraps(test_method)
        def inner(test_class_instance, *args, **kwargs):
            test_class_instance.client.login(username=username, password=password)
            test_method(test_class_instance, *args, **kwargs)
            test_class_instance.client.logout()
        return inner
    return decorator