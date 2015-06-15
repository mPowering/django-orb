'''
Script to validate urls
'''
import django
import time
import urllib2 
from django.conf import settings
from orb.models import ResourceURL, Tag
from orb.emailer import link_checker_results


def run(): 
    from orb.api.error_codes import HTML_OK

    resource_urls = []
    
    urls = ResourceURL.objects.all()
    for u in urls:
        time.sleep(1)
        handler = urllib2.HTTPHandler()
        opener = urllib2.build_opener(handler)
        request = urllib2.Request(u.url )
        request.add_header("User-Agent",'ORB Link Validator')
        
        try:
            connection = opener.open(request)
        except:
            #connection = e
            resource_urls.append(u)
            continue

        print u.url + " : " + str(connection.code)
  

    tags = []
    
    urls = Tag.objects.exclude(external_url=None).exclude(external_url='')
    for u in urls:
        time.sleep(1)
        
        handler = urllib2.HTTPHandler()
        opener = urllib2.build_opener(handler)
        request = urllib2.Request(u.external_url )
        request.add_header("User-Agent",'ORB Link Validator')
        try:
            connection = opener.open(request)
        except urllib2.HTTPError,e:
            connection = e
            tags.append(u)
            continue

        print u.external_url + " : " + str(connection.code)
    
    print resource_urls
    print tags
    
    if len(resource_urls) > 0 or len(tags) > 0:
        link_checker_results(resource_urls, tags)

if __name__ == "__main__":
    django.setup()
    run() 
    
    
    


