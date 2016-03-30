# orb/toolkit/views.py
from django.shortcuts import render_to_response
from django.template import RequestContext


def toolkit_home_view(request):

    return render_to_response('orb/toolkits/home.html',
                              {
                              },
                              context_instance=RequestContext(request))
