# orb/toolkit/views.py
from django.conf import settings
from django.http import Http404, HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.template import RequestContext

def toolkit_home_view(request):
    
    
    return render_to_response('orb/toolkit/home.html',
                              {
                               },
                              context_instance=RequestContext(request))



 
    