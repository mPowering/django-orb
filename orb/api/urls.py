
from django.conf.urls import patterns, include, url
from tastypie.api import Api

from orb.api.resources import ResourceResource, TagResource, ResourceTagResource, ResourceFileResource, ResourceURLResource

v1_api = Api(api_name='v1')
v1_api.register(ResourceResource())
v1_api.register(TagResource())
v1_api.register(ResourceTagResource())
v1_api.register(ResourceURLResource())
v1_api.register(ResourceFileResource())

urlpatterns = patterns('',

    url(r'^', include(v1_api.urls)),
    url(r'^upload/image/$', 'orb.api.upload.image_view', name="orb_image_upload"),
    url(r'^upload/file/$', 'orb.api.upload.file_view', name="orb_file_upload"),
    
)