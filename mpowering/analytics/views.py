
import os 

from django.shortcuts import render,render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext as _


from PIL import Image


# Create your views here.


def home_view(request):
    
    return render_to_response('mpowering/analytics/home.html',
                              {},
                              context_instance=RequestContext(request))
