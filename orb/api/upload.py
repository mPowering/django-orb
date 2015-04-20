import os

from django.conf import settings
from django.contrib.auth import authenticate
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import render,render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext as _
from django.views.decorators.csrf import csrf_exempt

from orb.models import Resource, ResourceFile

from tastypie.authentication import ApiKeyAuthentication
from tastypie.exceptions import BadRequest

@csrf_exempt
def image_view(request):
    
    if request.method != 'POST':
        return HttpResponse(status=405)
    
    auth = ApiKeyAuthentication()
    auth_result = auth.is_authenticated(request)
    if auth_result == False:
        return HttpResponse(status=401)
    elif auth_result != True:
        return auth_result

    required_params = ['resource_id']
    
    for r in required_params:
        if r not in request.POST:
            return HttpResponse(status=400, content='{ "error": "No '+r+' provided"}')
     
    if 'image_file' not in request.FILES:
       return HttpResponse(status=400, content='{ "error": "No image file provided"}')
      
    # check owner of resource
    resource_id = request.POST['resource_id']
    try:
        resource = Resource.objects.get(create_user=request.user,pk=resource_id)
    except Resource.DoesNotExist:
        return HttpResponse(status=401)
    
    # handle file upload
    resource.image = request.FILES['image_file']
    resource.save()
   
    return HttpResponse(status=200)


@csrf_exempt
def file_view(request):
    if request.method != 'POST':
        return HttpResponse(status=405)
    
    auth = ApiKeyAuthentication()
    auth_result = auth.is_authenticated(request)
    if auth_result == False:
        return HttpResponse(status=401)
    elif auth_result != True:
        return auth_result

    required_params = ['resource_id','title', 'description']
    
    for r in required_params:
        if r not in request.POST:
            return HttpResponse(status=400, content='{ "error": "No '+r+' provided"}')
     
    if 'resource_file' not in request.FILES:
       return HttpResponse(status=400, content='{ "error": "No resource file provided"}')
      
    # check owner of resource
    resource_id = request.POST['resource_id']
    try:
        resource = Resource.objects.get(create_user=request.user,pk=resource_id)
    except Resource.DoesNotExist:
        return HttpResponse(status=401)
    
    rf = ResourceFile()
    rf.title = request.POST['title']
    rf.resource = resource
    rf.create_user = request.user
    rf.update_user = request.user
    rf.file = request.FILES['resource_file']
    rf.description = request.POST['description']
    rf.save()
    
    return HttpResponse(status=201)