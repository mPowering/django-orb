'''
Script to validate urls
'''
import datetime
import django
import time
import urllib2 
from django.conf import settings
from orb.models import ResourceURL, Tag
from orb.emailer import link_checker_results


def run(): 
    from orb.api.error_codes import HTML_OK

    resource_urls = []
    today_number = datetime.datetime.today().weekday()
    
    urls = ResourceURL.objects.all()
    for u in urls:
        if u.id % 7 != today_number:
            continue
        
        time.sleep(10)
        req = urllib2.Request(u.url, headers={ 'User-Agent': 'ORB Link Validator', })
        try:
            response = urllib2.urlopen(req)
        except:
            resource_urls.append(u)
            continue

        print u.url + " : " + str(HTML_OK)
    tags = []
    
    urls = Tag.objects.exclude(external_url=None).exclude(external_url='')
    for u in urls:
        if u.id % 7 != today_number:
            continue
        
        time.sleep(10)
        req = urllib2.Request(u.external_url, headers={ 'User-Agent': 'Mozilla/5.0', })
        try:
            response = urllib2.urlopen(req)
        except Exception, e:
            tags.append(u)
            continue

        print u.external_url + " : " + str(HTML_OK)
    
    print resource_urls
    print tags
    
    if len(resource_urls) > 0 or len(tags) > 0:
        link_checker_results(resource_urls, tags)

if __name__ == "__main__":
    django.setup()
    run() 
    
    
    


