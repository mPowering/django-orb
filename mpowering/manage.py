import urllib2

from django.shortcuts import render_to_response
from django.template import RequestContext

from mpowering.models import ResourceURL





def check_urls_view(request):
    urls = ResourceURL.objects.all()
    output = []
    for u in urls:
        response = urllib2.Request(u.url)
        url = urlOpener.open(response)
    
    return render_to_response('mpowering/manage/urls.html',
                              {'urls': urls,},
                              context_instance=RequestContext(request))