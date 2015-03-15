import os

from django.conf import settings
from django.contrib.auth import authenticate
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import render,render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages

from tastypie.authentication import ApiKeyAuthentication


@csrf_exempt
def image_view(request):
    
    if request.method != 'POST':
        return HttpResponse(status=405)
    
    required = ['tags','is_draft']
   
    auth = ApiKeyAuthentication()
    auth_result = auth.is_authenticated(request)
    print auth.user()
    print auth_result
    #request.headers['Authorization'] = 'ApiKey %s:%s' % (username, api_key)
    #print username
    return HttpResponse(status=201)
    
    if not request.POST['username'] or not request.POST['api_key']:
        #return self._unauthorized()
        try:
            user = User.objects.get(username=request.POST['username'])
        except (User.DoesNotExist, User.MultipleObjectsReturned):
            #return self._unauthorized()
            pass
        
    for r in required:
        if r not in request.POST:
            print r + " not found"
            return HttpResponse(status=400)
   
    
    if 'course_file' not in request.FILES:
        print "Course file not found"
        return HttpResponse(status=400)
    
    return HttpResponse(status=201)


@csrf_exempt
def file_view(request):
    if request.method != 'POST':
        return HttpResponse(status=405)
    
    return HttpResponse(status=201)