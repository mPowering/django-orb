# orb.test_profile.py

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client

from orb.models import SearchTracker, ResourceTracker, TagTracker, UserProfile
from orb.profile.forms import RegisterForm
from orb.profile.views import build_form_options

from tastypie.models import ApiKey

class BasicTest(TestCase):
    def setUp(self):
        self.client = Client()
    
    def test_home(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
    
    
class RegisterTest(TestCase):
    fixtures = ['user.json', 'orb.json']
    new_user_data = {'username': 'newuser', 
                     'password': 'secret', 
                     'password_again': 'secret', 
                     'email': 'newuser@example.org', 
                     'first_name': 'demo',
                     'last_name': 'user',
                     'gender': 'none',
                     'age_range': 'none',
                     'mailing': 1,
                     'terms': 1,
                     'role_other': 'programmer',
                     'role': '0',
                     'organisation': 'My Organisation'}
    def setUp(self):
        self.client = Client()
        
    def test_register(self):
        no_users_start = User.objects.all().count()
        no_keys_start = ApiKey.objects.all().count()
        no_profiles_start = UserProfile.objects.all().count()
        
        response = self.client.post(reverse('profile_register'), self.new_user_data)
        self.assertEqual(response.status_code, 302)

        no_users_end = User.objects.all().count()
        no_keys_end = ApiKey.objects.all().count()
        no_profiles_end = UserProfile.objects.all().count()
        self.assertEqual(no_users_start+1, no_users_end)
        self.assertEqual(no_keys_start+1, no_keys_end)
        self.assertEqual(no_profiles_start+1, no_profiles_end)
        
    
    def test_register_with_no_data(self):
        response = self.client.post('/profile/register/', {})
        self.assertEqual(response.status_code, 200)
     
    def test_register_with_missing_data(self):
        no_users_start = User.objects.all().count()
        no_keys_start = ApiKey.objects.all().count()
        no_profiles_start = UserProfile.objects.all().count()
        
        response = self.client.post('/profile/register/', {})
        self.assertEqual(response.status_code, 200)
        
        no_users_end = User.objects.all().count()
        no_keys_end = ApiKey.objects.all().count()
        no_profiles_end = UserProfile.objects.all().count()
        self.assertEqual(no_users_start, no_users_end)
        self.assertEqual(no_keys_start, no_keys_end)
        self.assertEqual(no_profiles_start, no_profiles_end)
              
    def test_login(self):
        response = self.client.post('/profile/login/', {'username': 'demo', 'password': 'secret'})
        self.assertEqual(response.status_code, 200)

'''
TODO: test:
- password update
- profile update
- password reset

'''
