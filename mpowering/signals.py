from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.dispatch import Signal

from mpowering.models import Tracker

resource_viewed = Signal(providing_args=["resource", "request"])
resource_url_viewed = Signal(providing_args=["resource_url", "request"])
resource_file_viewed = Signal(providing_args=["resource_file", "request"])

def resource_viewed_callback(sender, **kwargs):
    request = kwargs.get('request')
    resource = kwargs.get('resource')
    
    tracker = Tracker()
    if not request.user.is_anonymous():
        tracker.user = request.user
    tracker.resource = resource
    tracker.ip = request.META.get('REMOTE_ADDR','0.0.0.0')
    tracker.user_agent = request.META.get('HTTP_USER_AGENT','unknown')
    tracker.type = Tracker.VIEW
    tracker.save()
    return

def resource_url_viewed_callback(sender, **kwargs):
    request = kwargs.get('request')
    resource_url = kwargs.get('resource_url')
    
    tracker = Tracker()
    if not request.user.is_anonymous():
        tracker.user = request.user
    tracker.resource_url = resource_url
    tracker.ip = request.META.get('REMOTE_ADDR','0.0.0.0')
    tracker.user_agent = request.META.get('HTTP_USER_AGENT','unknown')
    tracker.type = Tracker.VIEW
    tracker.save()
    return

def resource_file_viewed_callback(sender, **kwargs):
    request = kwargs.get('request')
    resource_file = kwargs.get('resource_file')
    
    tracker = Tracker()
    if not request.user.is_anonymous():
        tracker.user = request.user
    tracker.resource_file = resource_file
    tracker.ip = request.META.get('REMOTE_ADDR','0.0.0.0')
    tracker.user_agent = request.META.get('HTTP_USER_AGENT','unknown')
    tracker.type = Tracker.VIEW
    tracker.save()
    return

resource_viewed.connect(resource_viewed_callback)
resource_url_viewed.connect(resource_url_viewed_callback)
resource_file_viewed.connect(resource_file_viewed_callback)