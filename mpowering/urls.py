# mpowering/urls.py
from django.conf import settings
from django.conf.urls import patterns, include, url


urlpatterns = patterns('',

    url(r'^$', 'mpowering.views.home_view', name="mpowering_home"),
    url(r'^tag/(?P<tag_slug>\w[\w/-]*)$', 'mpowering.views.tag_view', name="mpowering_tags"),
    url(r'^profile/', include('mpowering.profile.urls')),
    url(r'^resource/create/$', 'mpowering.views.resource_create_view', name="mpowering_resource_create"),
    url(r'^resource/create/(?P<id>\d+)/thanks/$', 'mpowering.views.resource_create_thanks_view', name="mpowering_resource_create_thanks"),
    url(r'^resource/view/(?P<resource_slug>\w[\w/-]*)$', 'mpowering.views.resource_view', name="mpowering_resource"),
    url(r'^resource/link/(?P<id>\d+)/$', 'mpowering.views.resource_link_view', name="mpowering_resource_view_link"),
    url(r'^resource/file/(?P<id>\d+)/$', 'mpowering.views.resource_file_view', name="mpowering_resource_view_file"),
    
    
    url(r'^tinymce/', include('tinymce.urls')),
    
)
