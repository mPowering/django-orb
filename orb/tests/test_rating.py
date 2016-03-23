# orb.test_rating.py

from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client

from orb.models import ResourceRating


class RatingTest(TestCase):
    fixtures = ['user.json', 'orb.json']

    def setUp(self):
        self.client = Client()

    def test_ratings(self):
        # check can't do a get request
        response = self.client.get(reverse('orb_rate'))
        self.assertEqual(response.status_code, 404)

        # check anon user can't post
        response = self.client.post(reverse('orb_rate'), None)
        self.assertEqual(response.status_code, 404)

        rating = {'resource_id': 5, 'rating': 5}
        response = self.client.post(reverse('orb_rate'), rating)
        self.assertEqual(response.status_code, 404)

        # check both resource_id and rating are required
        self.client.login(username='standarduser', password='password')
        rating = {'resource_id': 5}
        response = self.client.post(reverse('orb_rate'), rating)
        self.assertEqual(response.status_code, 400)

        rating = {'rating': 5}
        response = self.client.post(reverse('orb_rate'), rating)
        self.assertEqual(response.status_code, 400)

        rating = {}
        response = self.client.post(reverse('orb_rate'), rating)
        self.assertEqual(response.status_code, 400)

        rating = {}
        response = self.client.post(reverse('orb_rate'), None)
        self.assertEqual(response.status_code, 400)

        # check invalid resource_id
        rating = {'resource_id': 5555, 'rating': 5}
        response = self.client.post(reverse('orb_rate'), rating)
        self.assertEqual(response.status_code, 400)

        # check invalid rating score
        rating = {'resource_id': 5, 'rating': 6}
        response = self.client.post(reverse('orb_rate'), rating)
        self.assertEqual(response.status_code, 400)

        rating = {'resource_id': 5, 'rating': 0}
        response = self.client.post(reverse('orb_rate'), rating)
        self.assertEqual(response.status_code, 400)

        rating = {'resource_id': 5, 'rating': -1}
        response = self.client.post(reverse('orb_rate'), rating)
        self.assertEqual(response.status_code, 400)

        # check rating gets updated rather than as new
        rating = {'resource_id': 5, 'rating': 3}
        ratings_count_start = ResourceRating.objects.all().count()
        response = self.client.post(reverse('orb_rate'), rating)
        self.assertEqual(response.status_code, 200)
        ratings_count_end = ResourceRating.objects.all().count()
        self.assertEqual(ratings_count_start + 1, ratings_count_end)

        rating = {'resource_id': 5, 'rating': 5}
        ratings_count_start = ResourceRating.objects.all().count()
        response = self.client.post(reverse('orb_rate'), rating)
        ratings_count_end = ResourceRating.objects.all().count()
        self.assertEqual(ratings_count_start, ratings_count_end)

        self.client.logout()
