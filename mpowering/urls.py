# mpowering/urls.py
from django.conf import settings
from django.conf.urls import patterns, include, url


urlpatterns = patterns('',

    url(r'^$', 'mpowering.views.home_view', name="mpowering_home"),
    url(r'^tag/(?P<tag_slug>\w[\w/-]*)$', 'mpowering.views.tag_view', name="mpowering_tags"),
    url(r'^profile/', include('mpowering.profile.urls')),
    url(r'^resource/create/$', 'mpowering.views.resource_create_view', name="mpowering_resource_create"),
    url(r'^resource/view/(?P<resource_slug>\w[\w/-]*)$', 'mpowering.views.resource_view', name="mpowering_resource"),
    
)
