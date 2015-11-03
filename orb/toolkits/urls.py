# orb/urls.py
from django.conf import settings
from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView


urlpatterns = patterns('',
    
    
    url(r'^$', 'orb.toolkits.views.toolkit_home_view', name="orb_toolkits_home"),
    
)
