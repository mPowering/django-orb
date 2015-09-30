# orb/urls.py
from django.conf import settings
from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView


urlpatterns = patterns('',
    
    
    url(r'^$', 'orb.bookmark.views.resource_bookmark_view', name="orb_bookmark"),
    url(r'^remove/(?P<resource_id>\d+)/$', 'orb.bookmark.views.resource_bookmark_remove_view', name="orb_bookmark_remove"),
    
)
