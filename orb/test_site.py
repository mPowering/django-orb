# orb.test_site.py

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client

from orb.models import Tag, Resource

class SiteTest(TestCase):
    fixtures = ['user.json', 'orb.json']
    
    def setUp(self):
        self.client = Client()
    
    def test_pages(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        
        response = self.client.get(reverse('orb_about'))
        self.assertEqual(response.status_code, 200)
        
        response = self.client.get(reverse('orb_developers'))
        self.assertEqual(response.status_code, 200)
        
        response = self.client.get(reverse('orb_how_to'))
        self.assertEqual(response.status_code, 200)
        
        response = self.client.get(reverse('orb_partners'))
        self.assertEqual(response.status_code, 200)  

        response = self.client.get(reverse('orb_taxonomy'))
        self.assertEqual(response.status_code, 200)  

        response = self.client.get(reverse('orb_terms'))
        self.assertEqual(response.status_code, 200) 
        
        response = self.client.get(reverse('orb_tag_cloud'))
        self.assertEqual(response.status_code, 200)
        
        response = self.client.get(reverse('orb_tags_filter'))
        self.assertEqual(response.status_code, 200)
        
        response = self.client.get(reverse('orb_resource_create'))
        self.assertEqual(response.status_code, 200)
        
        response = self.client.get(reverse('orb_guidelines'))
        self.assertEqual(response.status_code, 200)
        
        response = self.client.get(reverse('orb_search'))
        self.assertEqual(response.status_code, 200)
        
        response = self.client.get(reverse('orb_search_advanced'))
        self.assertEqual(response.status_code, 200)
        
        response = self.client.get(reverse('orb_opensearch'))
        self.assertEqual(response.status_code, 200)
        
    def test_tags(self):  
         
        tags = Tag.objects.all()
        
        for t in tags:
            print t.slug
            response = self.client.get(reverse('orb_tags', args=[t.slug]))
            self.assertEqual(response.status_code, 200)
    
    def test_resources_approved(self):
        
        approved_resources = Resource.objects.filter(status=Resource.APPROVED)
        
        for r in approved_resources:
            
            # Anon user (not logged in)
            response = self.client.get(reverse('orb_resource', args=[r.slug]))
            self.assertEqual(response.status_code, 200) 
            
            response = self.client.get(reverse('orb_resource_permalink', args=[r.id]))
            self.assertEqual(response.status_code, 200) 
            
            # Standard user
            self.client.login(username='standarduser', password='password')
            response = self.client.get(reverse('orb_resource', args=[r.slug]))
            self.assertEqual(response.status_code, 200) 
            
            response = self.client.get(reverse('orb_resource_permalink', args=[r.id]))
            self.assertEqual(response.status_code, 200) 
            self.client.logout()
            
            # api user
            self.client.login(username='apiuser', password='password')
            response = self.client.get(reverse('orb_resource', args=[r.slug]))
            self.assertEqual(response.status_code, 200) 
            
            response = self.client.get(reverse('orb_resource_permalink', args=[r.id]))
            self.assertEqual(response.status_code, 200) 
            self.client.logout()
            
            # superuser
            self.client.login(username='superuser', password='password')
            response = self.client.get(reverse('orb_resource', args=[r.slug]))
            self.assertEqual(response.status_code, 200) 
            
            response = self.client.get(reverse('orb_resource_permalink', args=[r.id]))
            self.assertEqual(response.status_code, 200) 
            self.client.logout()
            
            # staffuser
            self.client.login(username='staffuser', password='password')
            response = self.client.get(reverse('orb_resource', args=[r.slug]))
            self.assertEqual(response.status_code, 200) 
            
            response = self.client.get(reverse('orb_resource_permalink', args=[r.id]))
            self.assertEqual(response.status_code, 200) 
            self.client.logout()
            
            # orgowner
            self.client.login(username='orgowner', password='password')
            response = self.client.get(reverse('orb_resource', args=[r.slug]))
            self.assertEqual(response.status_code, 200) 
            
            response = self.client.get(reverse('orb_resource_permalink', args=[r.id]))
            self.assertEqual(response.status_code, 200) 
            self.client.logout()
    
    def test_resources_pending_crt(self):    
        pending_crt_resources = Resource.objects.filter(status=Resource.PENDING_CRT)
        
        for r in pending_crt_resources:
            
            # Anon user (not logged in)
            response = self.client.get(reverse('orb_resource', args=[r.slug]))
            self.assertEqual(response.status_code, 404) 
            
            response = self.client.get(reverse('orb_resource_permalink', args=[r.id]))
            self.assertEqual(response.status_code, 404) 
            
            # Standard user
            self.client.login(username='standarduser', password='password')
            self.user = User.objects.get(username='standarduser')
            response = self.client.get(reverse('orb_resource', args=[r.slug]))
            if r.create_user == self.user or r.update_user == self.user:
                self.assertEqual(response.status_code, 200)
            else:
                self.assertEqual(response.status_code, 404)
            
            response = self.client.get(reverse('orb_resource_permalink', args=[r.id]))
            if r.create_user == self.user or r.update_user == self.user:
                self.assertEqual(response.status_code, 200)
            else:
                self.assertEqual(response.status_code, 404) 
            self.client.logout()
            
            # api user
            self.client.login(username='apiuser', password='password')
            self.user = User.objects.get(username='apiuser')
            response = self.client.get(reverse('orb_resource', args=[r.slug]))
            if r.create_user == self.user or r.update_user == self.user:
                self.assertEqual(response.status_code, 200)
            else:
                self.assertEqual(response.status_code, 404)
            
            response = self.client.get(reverse('orb_resource_permalink', args=[r.id]))
            if r.create_user == self.user or r.update_user == self.user:
                self.assertEqual(response.status_code, 200)
            else:
                self.assertEqual(response.status_code, 404) 
            self.client.logout()
            
            # superuser
            self.client.login(username='superuser', password='password')
            response = self.client.get(reverse('orb_resource', args=[r.slug]))
            self.assertEqual(response.status_code, 200) 
            
            response = self.client.get(reverse('orb_resource_permalink', args=[r.id]))
            self.assertEqual(response.status_code, 200) 
            self.client.logout()
            
            # staffuser
            self.client.login(username='staffuser', password='password')
            response = self.client.get(reverse('orb_resource', args=[r.slug]))
            self.assertEqual(response.status_code, 200) 
            
            response = self.client.get(reverse('orb_resource_permalink', args=[r.id]))
            self.assertEqual(response.status_code, 200) 
            self.client.logout()
            
            # orgowner
            self.client.login(username='orgowner', password='password')
            self.user = User.objects.get(username='orgowner')
            response = self.client.get(reverse('orb_resource', args=[r.slug]))
            if r.create_user == self.user or r.update_user == self.user:
                self.assertEqual(response.status_code, 200)
            else:
                self.assertEqual(response.status_code, 404)
            
            response = self.client.get(reverse('orb_resource_permalink', args=[r.id]))
            if r.create_user == self.user or r.update_user == self.user:
                self.assertEqual(response.status_code, 200)
            else:
                self.assertEqual(response.status_code, 404)
            self.client.logout()
        
    def test_resources_pending_mep(self): 
        pending_mep_resources = Resource.objects.filter(status=Resource.PENDING_MRT)
        
        for r in pending_mep_resources:
            
            # Anon user (not logged in)
            response = self.client.get(reverse('orb_resource', args=[r.slug]))
            self.assertEqual(response.status_code, 404) 
            
            response = self.client.get(reverse('orb_resource_permalink', args=[r.id]))
            self.assertEqual(response.status_code, 404) 
            
            # Standard user
            self.client.login(username='standarduser', password='password')
            self.user = User.objects.get(username='standarduser')
            response = self.client.get(reverse('orb_resource', args=[r.slug]))
            if r.create_user == self.user or r.update_user == self.user:
                self.assertEqual(response.status_code, 200)
            else:
                self.assertEqual(response.status_code, 404)
            
            response = self.client.get(reverse('orb_resource_permalink', args=[r.id]))
            if r.create_user == self.user or r.update_user == self.user:
                self.assertEqual(response.status_code, 200)
            else:
                self.assertEqual(response.status_code, 404) 
            self.client.logout()
            
            # api user
            self.client.login(username='apiuser', password='password')
            self.user = User.objects.get(username='apiuser')
            response = self.client.get(reverse('orb_resource', args=[r.slug]))
            if r.create_user == self.user or r.update_user == self.user:
                self.assertEqual(response.status_code, 200)
            else:
                self.assertEqual(response.status_code, 404)
            
            response = self.client.get(reverse('orb_resource_permalink', args=[r.id]))
            if r.create_user == self.user or r.update_user == self.user:
                self.assertEqual(response.status_code, 200)
            else:
                self.assertEqual(response.status_code, 404) 
            self.client.logout()
            
            # superuser
            self.client.login(username='superuser', password='password')
            response = self.client.get(reverse('orb_resource', args=[r.slug]))
            self.assertEqual(response.status_code, 200) 
            
            response = self.client.get(reverse('orb_resource_permalink', args=[r.id]))
            self.assertEqual(response.status_code, 200) 
            self.client.logout()
            
            # staffuser
            self.client.login(username='staffuser', password='password')
            response = self.client.get(reverse('orb_resource', args=[r.slug]))
            self.assertEqual(response.status_code, 200) 
            
            response = self.client.get(reverse('orb_resource_permalink', args=[r.id]))
            self.assertEqual(response.status_code, 200) 
            self.client.logout()
            
            # orgowner
            self.client.login(username='orgowner', password='password')
            self.user = User.objects.get(username='orgowner')
            response = self.client.get(reverse('orb_resource', args=[r.slug]))
            if r.create_user == self.user or r.update_user == self.user:
                self.assertEqual(response.status_code, 200)
            else:
                self.assertEqual(response.status_code, 404)
            
            response = self.client.get(reverse('orb_resource_permalink', args=[r.id]))
            if r.create_user == self.user or r.update_user == self.user:
                self.assertEqual(response.status_code, 200)
            else:
                self.assertEqual(response.status_code, 404)
            self.client.logout()
    
    def test_resources_rejected(self): 
            
        rejected_resources = Resource.objects.filter(status=Resource.REJECTED)
        
        for r in rejected_resources:
            
            # Anon user (not logged in)
            response = self.client.get(reverse('orb_resource', args=[r.slug]))
            self.assertEqual(response.status_code, 404) 
            
            response = self.client.get(reverse('orb_resource_permalink', args=[r.id]))
            self.assertEqual(response.status_code, 404) 
            
            # Standard user
            self.client.login(username='standarduser', password='password')
            self.user = User.objects.get(username='standarduser')
            response = self.client.get(reverse('orb_resource', args=[r.slug]))
            if r.create_user == self.user or r.update_user == self.user:
                self.assertEqual(response.status_code, 200)
            else:
                self.assertEqual(response.status_code, 404)
            
            response = self.client.get(reverse('orb_resource_permalink', args=[r.id]))
            if r.create_user == self.user or r.update_user == self.user:
                self.assertEqual(response.status_code, 200)
            else:
                self.assertEqual(response.status_code, 404) 
            self.client.logout()
            
            # api user
            self.client.login(username='apiuser', password='password')
            self.user = User.objects.get(username='apiuser')
            response = self.client.get(reverse('orb_resource', args=[r.slug]))
            if r.create_user == self.user or r.update_user == self.user:
                self.assertEqual(response.status_code, 200)
            else:
                self.assertEqual(response.status_code, 404)
            
            response = self.client.get(reverse('orb_resource_permalink', args=[r.id]))
            if r.create_user == self.user or r.update_user == self.user:
                self.assertEqual(response.status_code, 200)
            else:
                self.assertEqual(response.status_code, 404) 
            self.client.logout()
            
            # superuser
            self.client.login(username='superuser', password='password')
            response = self.client.get(reverse('orb_resource', args=[r.slug]))
            self.assertEqual(response.status_code, 200) 
            
            response = self.client.get(reverse('orb_resource_permalink', args=[r.id]))
            self.assertEqual(response.status_code, 200) 
            self.client.logout()
            
            # staffuser
            self.client.login(username='staffuser', password='password')
            response = self.client.get(reverse('orb_resource', args=[r.slug]))
            self.assertEqual(response.status_code, 200) 
            
            response = self.client.get(reverse('orb_resource_permalink', args=[r.id]))
            self.assertEqual(response.status_code, 200) 
            self.client.logout()
            
            # orgowner
            self.client.login(username='orgowner', password='password')
            self.user = User.objects.get(username='orgowner')
            response = self.client.get(reverse('orb_resource', args=[r.slug]))
            if r.create_user == self.user or r.update_user == self.user:
                self.assertEqual(response.status_code, 200)
            else:
                self.assertEqual(response.status_code, 404)
            
            response = self.client.get(reverse('orb_resource_permalink', args=[r.id]))
            if r.create_user == self.user or r.update_user == self.user:
                self.assertEqual(response.status_code, 200)
            else:
                self.assertEqual(response.status_code, 404)
            self.client.logout()
        
        '''
        orb_tags
        orb_tags_filter_prefill
        orb_tags_filter_results
        orb_tag_view_link
        orb_resource_create_thanks
        orb_resource
        orb_resource_permalink
        orb_resource_view_link
        orb_resource_view_file
        orb_resource_edit
        orb_resource_edit_thanks
        orb_resource_approve
        orb_resource_pending_mep
        orb_resource_reject
        orb_resource_reject_sent
        orb_search_advanced_results
        search results
 
 
        '''
 

 
class AnalyticsPageTest(TestCase):
    fixtures = ['user.json', 'orb.json']
    
    def setUp(self):
        self.client = Client()
        
    def test_pages(self):   
        
        # for anon user    
        response = self.client.get(reverse('orb_analytics_home'))
        self.assertEqual(response.status_code, 401) 
        
        response = self.client.get(reverse('orb_analytics_map'))
        self.assertEqual(response.status_code, 401) 
        
        # Standard user
        self.client.login(username='standarduser', password='password')
        response = self.client.get(reverse('orb_analytics_home'))
        self.assertEqual(response.status_code, 401) 
        
        response = self.client.get(reverse('orb_analytics_map'))
        self.assertEqual(response.status_code, 401) 
        self.client.logout()
        
        # api user
        self.client.login(username='apiuser', password='password')
        response = self.client.get(reverse('orb_analytics_home'))
        self.assertEqual(response.status_code, 401) 
        
        response = self.client.get(reverse('orb_analytics_map'))
        self.assertEqual(response.status_code, 401)
        self.client.logout()
        
        # superuser
        self.client.login(username='superuser', password='password')
        response = self.client.get(reverse('orb_analytics_home'))
        self.assertEqual(response.status_code, 200) 
        
        response = self.client.get(reverse('orb_analytics_map'))
        self.assertEqual(response.status_code, 200) 
        self.client.logout()
        
        # staffuser
        self.client.login(username='staffuser', password='password')
        response = self.client.get(reverse('orb_analytics_home'))
        self.assertEqual(response.status_code, 200) 
        
        response = self.client.get(reverse('orb_analytics_map'))
        self.assertEqual(response.status_code, 200)
        self.client.logout()
        
        # orgowner
        self.client.login(username='orgowner', password='password')
        response = self.client.get(reverse('orb_analytics_home'))
        self.assertEqual(response.status_code, 401) 
        
        response = self.client.get(reverse('orb_analytics_map'))
        self.assertEqual(response.status_code, 401)
        self.client.logout()
    
    
    def test_tags(self):
            
        tags = Tag.objects.all()
        for t in tags:
            # for anon user    
            response = self.client.get(reverse('orb_analytics_tag',args=[t.id]))
            self.assertEqual(response.status_code, 401)
        
            # Standard user
            self.client.login(username='standarduser', password='password')
            response = self.client.get(reverse('orb_analytics_tag',args=[t.id]))
            self.assertEqual(response.status_code, 401)
            self.client.logout()
            
            # api user
            self.client.login(username='apiuser', password='password')
            response = self.client.get(reverse('orb_analytics_tag',args=[t.id]))
            self.assertEqual(response.status_code, 401)
            self.client.logout()
            
            # superuser
            self.client.login(username='superuser', password='password')
            response = self.client.get(reverse('orb_analytics_tag',args=[t.id]))
            self.assertEqual(response.status_code, 200)
            self.client.logout()
            
            # staffuser
            self.client.login(username='staffuser', password='password')
            response = self.client.get(reverse('orb_analytics_tag',args=[t.id]))
            self.assertEqual(response.status_code, 200)
            self.client.logout()
            
            # orgowner
            self.client.login(username='orgowner', password='password')
            response = self.client.get(reverse('orb_analytics_tag',args=[t.id]))
            self.assertEqual(response.status_code, 200)
            self.client.logout()
         
        '''
        response = self.client.get(reverse('orb_analytics_download'))
        self.assertEqual(response.status_code, 401)     
        '''
                      
class FeedTest(TestCase):
    fixtures = ['user.json', 'orb.json']
    
    def setUp(self):
        self.client = Client()
        
        
    '''
    orb_feed
    orb_tag_feed
    '''