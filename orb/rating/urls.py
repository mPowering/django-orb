# orb/urls.py
from django.conf import settings
from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView


urlpatterns = patterns('',
    
    
    url(r'^$', 'orb.rating.views.resource_rate_view', name="orb_rate"),
    
)
