# mpowering/urls.py
from django.conf import settings
from django.conf.urls import patterns, include, url

from mpowering.api.resources import ResourceResource, TagsResource

from tastypie.api import Api

v1_api = Api(api_name='v1')
v1_api.register(ResourceResource())
v1_api.register(TagsResource())

urlpatterns = patterns('',

    url(r'^$', 'mpowering.views.home_view', name="mpowering_home"),
    url(r'^tag/(?P<tag_slug>\w[\w/-]*)$', 'mpowering.views.tag_view', name="mpowering_tags"),
    url(r'^profile/', include('mpowering.profile.urls')),
    url(r'^resource/create/$', 'mpowering.views.resource_create_view', name="mpowering_resource_create"),
    url(r'^resource/create/(?P<id>\d+)/thanks/$', 'mpowering.views.resource_create_thanks_view', name="mpowering_resource_create_thanks"),
    url(r'^resource/view/(?P<resource_slug>\w[\w/-]*)$', 'mpowering.views.resource_view', name="mpowering_resource"),
    url(r'^resource/link/(?P<id>\d+)/$', 'mpowering.views.resource_link_view', name="mpowering_resource_view_link"),
    url(r'^resource/file/(?P<id>\d+)/$', 'mpowering.views.resource_file_view', name="mpowering_resource_view_file"),
    url(r'^resource/edit/(?P<resource_id>\d+)/$', 'mpowering.views.resource_edit_view', name="mpowering_resource_edit"),
    url(r'^resource/edit/(?P<id>\d+)/thanks/$', 'mpowering.views.resource_edit_thanks_view', name="mpowering_resource_edit_thanks"),
    url(r'^resource/image/(?P<resource_id>\d+)/(?P<size>\d+)/$', 'mpowering.views.resource_thumbnail_view', name="mpowering_resource_image"),
    url(r'^resource/rate/$', 'mpowering.views.resource_rate_view', name="mpowering_resource_rate"),
    
    url(r'^tinymce/', include('tinymce.urls')),
    url(r'^search/$', 'mpowering.views.search_view', name="mpowering_search"),
    
    url(r'^api/', include(v1_api.urls)),
    
)
