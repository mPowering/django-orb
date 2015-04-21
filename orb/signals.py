import json

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.dispatch import Signal

from orb.emailer import first_resource
from orb.models import ResourceTracker, SearchTracker, ResourceWorkflowTracker
from orb.lib.search_crawler import is_search_crawler

resource_viewed = Signal(providing_args=["resource", "request", "type"])
resource_workflow = Signal(providing_args=["request", "resource", "status", "notes"])
resource_url_viewed = Signal(providing_args=["resource_url", "request"])
resource_file_viewed = Signal(providing_args=["resource_file", "request"])
search = Signal(providing_args=["query", "no_results", "request"])

def resource_viewed_callback(sender, **kwargs):
    request = kwargs.get('request')
    resource = kwargs.get('resource')
    type = kwargs.get('type')
    if is_search_crawler(request.META.get('HTTP_USER_AGENT','unknown')):
        return 
    
    if type is None:
        type = ResourceTracker.VIEW
        
    tracker = ResourceTracker()
    if not request.user.is_anonymous():
        tracker.user = request.user
    tracker.resource = resource
    tracker.ip = request.META.get('REMOTE_ADDR','0.0.0.0')
    tracker.user_agent = request.META.get('HTTP_USER_AGENT','unknown')
    tracker.type = type
    tracker.save()
    return

def resource_workflow_callback(sender, **kwargs):
    request = kwargs.get('request')
    resource = kwargs.get('resource')
    status = kwargs.get('status')
    notes = kwargs.get('notes')
    
    email_sent = False
    # if status is pending CRT (i.e new) and owner hasn't submitted before then send email
    if status == ResourceWorkflowTracker.PENDING_CRT:
        no_previous_resources = ResourceWorkflowTracker.objects.filter(create_user=request.user).count()
        if no_previous_resources == 0:
            first_resource(request.user, resource)
            email_sent = True
    
    # if approved
    if status == ResourceWorkflowTracker.APPROVED:
        pass
    
    # if passed to MEP
    if status == ResourceWorkflowTracker.PENDING_MEP:
        pass
    
    # if rejected
    if status == ResourceWorkflowTracker.REJECTED:
        pass
            
    # add a record to workflow tracker
    workflow_tracker = ResourceWorkflowTracker()
    workflow_tracker.resource = resource
    workflow_tracker.create_user = request.user
    workflow_tracker.status = status
    workflow_tracker.owner_email_sent = email_sent
    workflow_tracker.notes = notes
    workflow_tracker.save()
    
    return

def resource_url_viewed_callback(sender, **kwargs):
    request = kwargs.get('request')
    resource_url = kwargs.get('resource_url')
    if is_search_crawler(request.META.get('HTTP_USER_AGENT','unknown')):
        return 
    
    tracker = ResourceTracker()
    if not request.user.is_anonymous():
        tracker.user = request.user
    tracker.resource_url = resource_url
    tracker.resource = resource_url.resource
    tracker.ip = request.META.get('REMOTE_ADDR','0.0.0.0')
    tracker.user_agent = request.META.get('HTTP_USER_AGENT','unknown')
    tracker.type = ResourceTracker.VIEW
    tracker.save()
    return

def resource_file_viewed_callback(sender, **kwargs):
    request = kwargs.get('request')
    resource_file = kwargs.get('resource_file')
    
    if is_search_crawler(request.META.get('HTTP_USER_AGENT','unknown')):
        return 
    
    tracker = ResourceTracker()
    if not request.user.is_anonymous():
        tracker.user = request.user
    tracker.resource_file = resource_file
    tracker.resource = resource_file.resource
    tracker.ip = request.META.get('REMOTE_ADDR','0.0.0.0')
    tracker.user_agent = request.META.get('HTTP_USER_AGENT','unknown')
    tracker.type = ResourceTracker.VIEW
    tracker.save()
    return

def search_callback(sender, **kwargs):
    request = kwargs.get('request')
    query = kwargs.get('query')
    no_results = kwargs.get('no_results')
    
    if is_search_crawler(request.META.get('HTTP_USER_AGENT','unknown')):
        return 
    
    tracker = SearchTracker()
    if not request.user.is_anonymous():
        tracker.user = request.user
    tracker.query = query
    tracker.no_results = no_results
    tracker.ip = request.META.get('REMOTE_ADDR','0.0.0.0')
    tracker.user_agent = request.META.get('HTTP_USER_AGENT','unknown')
    tracker.save()
    return
 
resource_viewed.connect(resource_viewed_callback)
resource_workflow.connect(resource_workflow_callback)
resource_url_viewed.connect(resource_url_viewed_callback)
resource_file_viewed.connect(resource_file_viewed_callback)
search.connect(search_callback)