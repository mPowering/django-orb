from functools import wraps
from contextlib import contextmanager

from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client, RequestFactory

from orb.models import ResourceRating, Resource
from orb.tests.utils import request_factory


def login_client(username, password):
    """
    A decorator for test methods that logs in a user and logs out for
    the duration of the test method.

    Ought to be a context manager (too)!
    """
    def decorator(test_method):
        @wraps(test_method)
        def inner(test_class_instance, *args, **kwargs):
            test_class_instance.client.login(username=username, password=password)
            test_method(test_class_instance, *args, **kwargs)
            test_class_instance.client.logout()
        return inner
    return decorator


class RatingTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super(RatingTest, cls).setUpClass()
        cls.rating_user = User.objects.create_user(
            username="rating_user",
            email="rater@example.com",
            password="password",
        )
        cls.other_user = get_user_model().objects.create_user(
            username="other_user",
            email="other@example.com",
            password="password",
        )
        cls.resource = Resource.objects.create(
            title="Test resource",
            description="Test description",
            create_user=cls.rating_user,
            update_user=cls.rating_user,
        )

    def test_get_requests(self):
        """check can't do a get request"""
        response = self.client.get(reverse('orb_rate'))
        self.assertEqual(response.status_code, 404)

    def test_anon_users(self):
        """check anon user can't post"""
        response = self.client.post(reverse('orb_rate'), None)
        self.assertEqual(response.status_code, 404)

    def test_ratings(self):
        rating = {'resource_id': self.resource.pk, 'rating': 5}
        response = self.client.post(reverse('orb_rate'), rating)
        self.assertEqual(response.status_code, 404)

    @login_client(username='rating_user', password='password')
    def test_missing_data(self):
        """check both resource_id and rating are required"""
        rating = {'resource_id': self.resource.pk}
        response = self.client.post(reverse('orb_rate'), rating)
        self.assertEqual(response.status_code, 400)

        rating = {'resource_id': self.resource.pk}
        response = self.client.post(reverse('orb_rate'), rating)
        self.assertEqual(response.status_code, 400)

        response = self.client.post(reverse('orb_rate'), {})
        self.assertEqual(response.status_code, 400)

        response = self.client.post(reverse('orb_rate'), None)
        self.assertEqual(response.status_code, 400)

    @login_client(username='rating_user', password='password')
    def test_missing_resource(self):
        # check invalid resource_id
        rating = {'resource_id': 5555, 'rating': 5}
        response = self.client.post(reverse('orb_rate'), rating)
        self.assertEqual(response.status_code, 400)

    @login_client(username='rating_user', password='password')
    def test_invalid_score(self):
        # check invalid rating score
        rating = {'resource_id': self.resource.pk, 'rating': 6}
        response = self.client.post(reverse('orb_rate'), rating)
        self.assertEqual(response.status_code, 400)

        rating = {'resource_id': self.resource.pk, 'rating': 0}
        response = self.client.post(reverse('orb_rate'), rating)
        self.assertEqual(response.status_code, 400)

        rating = {'resource_id': self.resource.pk, 'rating': -1}
        response = self.client.post(reverse('orb_rate'), rating)
        self.assertEqual(response.status_code, 400)

    @login_client(username='rating_user', password='password')
    def test_rating_updated(self):
        """check rating gets updated rather than as new"""
        rating = {'resource_id': self.resource.pk, 'rating': 3}
        ratings_count_start = ResourceRating.objects.all().count()
        response = self.client.post(reverse('orb_rate'), rating)
        self.assertEqual(response.status_code, 200)
        ratings_count_end = ResourceRating.objects.all().count()
        self.assertEqual(ratings_count_start + 1, ratings_count_end)

        rating = {'resource_id': self.resource.pk, 'rating': 5}
        ratings_count_start = ResourceRating.objects.all().count()
        response = self.client.post(reverse('orb_rate'), rating)
        ratings_count_end = ResourceRating.objects.all().count()
        self.assertEqual(ratings_count_start, ratings_count_end)
