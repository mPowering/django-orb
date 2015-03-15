# mpowering/urls.py
from django.conf import settings
from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

from mpowering.api.resources import ResourceResource, TagResource, ResourceTagResource, ResourceURLResource
from mpowering.feeds import LatestTagEntries, LatestEntries

from tastypie.api import Api


v1_api = Api(api_name='v1')
v1_api.register(ResourceResource())
v1_api.register(TagResource())
v1_api.register(ResourceTagResource())
v1_api.register(ResourceURLResource())

urlpatterns = patterns('',

    url(r'^$', 'mpowering.views.home_view', name="mpowering_home"),
    url(r'^feed/$', LatestEntries() , name="mpowering_feed"),
    url(r'^tag/view/(?P<tag_slug>\w[\w/-]*)$', 'mpowering.views.tag_view', name="mpowering_tags"),
    url(r'^tag/cloud/$', 'mpowering.views.tag_cloud_view', name="mpowering_tag_cloud"),
    url(r'^tag/feed/(?P<tag_slug>\w[\w/-]*)$', LatestTagEntries() , name="mpowering_tag_feed"),
    url(r'^tag/filter/$', 'mpowering.views.tag_filter_view', name="mpowering_tags_filter"),
    url(r'^tag/filter/results$', 'mpowering.views.tag_filter_results_view', name="mpowering_tags_filter_results"),
    url(r'^profile/', include('mpowering.profile.urls')),
    url(r'^resource/create/$', 'mpowering.views.resource_create_view', name="mpowering_resource_create"),
    url(r'^resource/create/(?P<id>\d+)/thanks/$', 'mpowering.views.resource_create_thanks_view', name="mpowering_resource_create_thanks"),
    url(r'^resource/view/(?P<resource_slug>\w[\w/-]*)$', 'mpowering.views.resource_view', name="mpowering_resource"),
    url(r'^resource/(?P<id>\d+)$', 'mpowering.views.resource_permalink_view', name="mpowering_resource_permalink"),
    url(r'^resource/link/(?P<id>\d+)/$', 'mpowering.views.resource_link_view', name="mpowering_resource_view_link"),
    url(r'^resource/file/(?P<id>\d+)/$', 'mpowering.views.resource_file_view', name="mpowering_resource_view_file"),
    url(r'^resource/edit/(?P<resource_id>\d+)/$', 'mpowering.views.resource_edit_view', name="mpowering_resource_edit"),
    url(r'^resource/edit/(?P<id>\d+)/thanks/$', 'mpowering.views.resource_edit_thanks_view', name="mpowering_resource_edit_thanks"),
   
    url(r'^resource/approve/(?P<id>\d+)/$', 'mpowering.views.resource_approve_view', name="mpowering_resource_approve"),
    url(r'^resource/reject/(?P<id>\d+)/$', 'mpowering.views.resource_reject_view', name="mpowering_resource_reject"),
    
    url(r'^resource/rate/$', 'mpowering.views.resource_rate_view', name="mpowering_resource_rate"),
    url(r'^resource/guidelines/$',TemplateView.as_view(template_name="mpowering/resource/guidelines.html"), name="mpowering_guidelines"),
    
    
    url(r'^analytics/', include('mpowering.analytics.urls')),
    
    url(r'^tinymce/', include('tinymce.urls')),
    url(r'^search/$', 'mpowering.views.search_view', name="mpowering_search"),
    url(r'^opensearch/$', TemplateView.as_view(template_name="search/opensearch.html"), name="mpowering_opensearch"),
    
    url(r'^api/', include(v1_api.urls)),
    url(r'^api/upload/image/$', 'mpowering.api.upload.image_view', name="mpowering_image_upload"),
    url(r'^api/upload/file/$', 'mpowering.api.upload.file_view', name="mpowering_file_upload"),
    
)
