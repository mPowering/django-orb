# orb/rating/views.py

from django.http import Http404, HttpResponse
from django.shortcuts import render,render_to_response
from django.template import RequestContext

def country_map_view(request):
    return render_to_response('orb/viz/country_map.html',
                              {},
                              context_instance=RequestContext(request))
    