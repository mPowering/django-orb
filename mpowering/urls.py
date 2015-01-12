# mpowering/urls.py
from django.conf import settings
from django.conf.urls import patterns, include, url


urlpatterns = patterns('',

    url(r'^$', 'mpowering.views.home_view', name="mpowering_home"),
    url(r'^tag/(?P<tag_slug>\w[\w/-]*)$', 'mpowering.views.tag_view', name="mpowering_tags"),
    url(r'^resource/(?P<resource_slug>\w[\w/-]*)$', 'mpowering.views.resource_view', name="mpowering_resource"),
    
)
