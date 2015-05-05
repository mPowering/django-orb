# orb.test_api.py

from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import Client

from orb.models import SearchTracker, ResourceTracker, TagTracker

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
            'username': 'standarduser',
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
        tracker_count_start = SearchTracker.objects.all().count()
        resp = self.api_client.get(self.url, format='json', data=self.auth_data)
        self.assertHttpOK(resp)
        self.assertValidJSON(resp.content)
        
        tracker_count_end = SearchTracker.objects.all().count()
        self.assertEqual(tracker_count_start+1, tracker_count_end)
   
    #check results are returned     
    def test_search_results(self):
        data = self.auth_data
        data['q'] = 'medical'
        
        resp = self.api_client.get(self.url, format='json', data=data)
        self.assertHttpOK(resp)
        self.assertValidJSON(resp.content)
        self.assertEqual(len(self.deserialize(resp)['objects']), 1)
      
     
    # check search request added to search tracker
       
        
# Resource API
class ResourceResourceTest(ResourceTestCase):
    fixtures = ['user.json', 'orb.json']
    
    def setUp(self):
        super(ResourceResourceTest, self).setUp()
        
        standard_user = User.objects.get(username='standarduser')
        api_key = ApiKey.objects.get(user = standard_user)
        self.standard_user = {
            'username': standard_user.username,
            'api_key': api_key.key,
        }
        
        api_user = User.objects.get(username='apiuser')
        api_key = ApiKey.objects.get(user = api_user)
        self.standard_user = {
            'username': api_user.username,
            'api_key': api_key.key,
        }
        
        self.url = '/api/v1/resource/'
        
    # check get allowed for valid user
    def test_get_valid(self):
        resp = self.api_client.get(self.url, format='json', data=self.standard_user)
        self.assertHttpOK(resp)
        self.assertValidJSON(resp.content)

    # check get allowed for valid user  
    def test_get_not_valid(self):
        self.assertHttpUnauthorized(self.api_client.get(self.url, format='json', data={}))
        
    # check post not allowed for invalid user
    def test_post_invalid(self):
        resp = self.api_client.post(self.url, format='json', data=self.standard_user)
        self.assertHttpUnauthorized(resp)
     
    # check put not allowed
    def test_put_invalid(self):
        resp = self.api_client.put(self.url, format='json', data=self.standard_user)
        self.assertHttpMethodNotAllowed(resp)
        
    # check delete not allowed
    def test_delete_invalid(self):
        resp = self.api_client.delete(self.url, format='json', data=self.standard_user)
        self.assertHttpMethodNotAllowed(resp) 
     
    # check put not allowed
    def test_put_invalid_api_user(self):
        resp = self.api_client.put(self.url, format='json', data=self.api_user)
        self.assertHttpMethodNotAllowed(resp)
        
    # check delete not allowed
    def test_delete_invalid_api_user(self):
        resp = self.api_client.delete(self.url, format='json', data=self.api_user)
        self.assertHttpMethodNotAllowed(resp)    
        
    def test_get_approved_resource(self):
        resp = self.api_client.get(self.url, format='json', data=self.standard_user)
        self.assertHttpMethodNotAllowed(resp) 
    '''
    Check:
    can't get an unapproved resource (unapproved is #125)
    any authorized user can get
    on user with api access can post
    delete not allowed
    put not allowed 
    check that tags are returned for the resources
       
    '''
        
# Tag API
class TagResourceTest(ResourceTestCase):
    fixtures = ['user.json', 'orb.json']
    
    def setUp(self):
        super(TagResourceTest, self).setUp()
        
        standard_user = User.objects.get(username='standarduser')
        api_key = ApiKey.objects.get(user = standard_user)
        self.standard_user = {
            'username': standard_user.username,
            'api_key': api_key.key,
        }
        
        api_user = User.objects.get(username='apiuser')
        api_key = ApiKey.objects.get(user = api_user)
        self.standard_user = {
            'username': api_user.username,
            'api_key': api_key.key,
        }
        
        self.url = '/api/v1/tag/'
        
# ResourceTag API
class ResourceTagResourceTest(ResourceTestCase):
    fixtures = ['user.json', 'orb.json']
    
    def setUp(self):
        super(ResourceTagResourceTest, self).setUp()
        
        standard_user = User.objects.get(username='standarduser')
        api_key = ApiKey.objects.get(user = standard_user)
        self.standard_user = {
            'username': standard_user.username,
            'api_key': api_key.key,
        }
        
        api_user = User.objects.get(username='apiuser')
        api_key = ApiKey.objects.get(user = api_user)
        self.standard_user = {
            'username': api_user.username,
            'api_key': api_key.key,
        }
        
        self.url = '/api/v1/resourcetag/'