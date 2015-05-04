# orb.test_api.py

from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import Client

from tastypie.models import ApiKey
from tastypie.test import ResourceTestCase

# Create your tests here.

# Search API
class SearchResourceTest(ResourceTestCase): 
    fixtures = ['user.json', 'orb.json']
    
    
    def setUp(self):
        super(SearchResourceTest, self).setUp()
        user = User.objects.get(username='demo5')
        api_key = ApiKey.objects.get(user = user)
        self.auth_data = {
            'username': 'demo5',
            'api_key': api_key.key,
        }
        self.url = '/api/v1/resource/search/'
        
    # check post not allowed
    def test_post_invalid(self):
        self.assertHttpMethodNotAllowed(self.api_client.post(self.url, format='json', data={}))
        
    # check unauthorized
    def test_unauthorized(self):
        data = {
            'username': 'user',
            'api_key': '1234',
        }
        self.assertHttpUnauthorized(self.api_client.get(self.url, format='json', data=data))
    
    # check authorized
    def test_authorized(self):
        resp = self.api_client.get(self.url, format='json', data=self.auth_data)
        self.assertHttpOK(resp)
        self.assertValidJSON(resp.content)
   
    #check results are returned     
    def test_search_results(self):
        data = self.auth_data
        data['q'] = 'medical'
        
        resp = self.api_client.get(self.url, format='json', data=data)
        self.assertHttpOK(resp)
        self.assertValidJSON(resp.content)
        self.assertEqual(len(self.deserialize(resp)['objects']), 1)
        
        
# Resource API
class ResourceResourceTest(ResourceTestCase):
    
    def setUp(self):
        super(SearchResourceTest, self).setUp()
        user = User.objects.get(username='demo5')
        api_key = ApiKey.objects.get(user = user)
        self.auth_data = {
            'username': 'demo5',
            'api_key': api_key.key,
        }
        self.url = '/api/v1/resource/'
        
    # check get allowed
    def test_get_valid(self):
        self.assertHttpMethodAllowed(self.api_client.get(self.url, format='json', data={}))
        
    '''
    Check:
    can't get an unapproved resource
    any authorized user can get
    on user with api access can post
    delete not allowed
    put not allowed 
    check that tags are returned for the resources
       
    '''