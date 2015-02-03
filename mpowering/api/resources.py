
from django.conf import settings
from django.core.urlresolvers import reverse

from tastypie import fields
from tastypie.authentication import Authentication,ApiKeyAuthentication
from tastypie.authorization import ReadOnlyAuthorization
from tastypie.models import ApiKey
from tastypie.resources import ModelResource

from mpowering.api.serializers import PrettyJSONSerializer, ResourceSerializer
from mpowering.models import Resource, ResourceOrganisation, Organisation, ResourceFile, ResourceURL, ResourceTag, Tag, Category

class ResourceResource(ModelResource):
    organisations = fields.ToManyField('mpowering.api.resources.ResourceOrganisationResource', 'resourceorganisation_set', related_name='resource', full=True)
    files = fields.ToManyField('mpowering.api.resources.ResourceFileResource', 'resourcefile_set', related_name='resource', full=True)
    urls = fields.ToManyField('mpowering.api.resources.ResourceURLResource', 'resourceurl_set', related_name='resource', full=True)
    tags = fields.ToManyField('mpowering.api.resources.ResourceTagResource', 'resourcetag_set', related_name='resource', full=True)
    class Meta:
        queryset = Resource.objects.filter(status=Resource.APPROVED)
        resource_name = 'resource'
        allowed_methods = ['get']
        authentication = ApiKeyAuthentication()
        authorization = ReadOnlyAuthorization() 
        serializer = ResourceSerializer()
        always_return_data = True 
        include_resource_uri = True

    def dehydrate_image(self,bundle):
        return get_full_url_prefix(bundle) + settings.MEDIA_URL + bundle.obj.image.name
    
class ResourceOrganisationResource(ModelResource):
    organisation = fields.ToOneField('mpowering.api.resources.OrganisationResource', 'organisation', full=True)
    class Meta:
        queryset = ResourceOrganisation.objects.all()
        allowed_methods = ['get']
        include_resource_uri = False
        authentication = ApiKeyAuthentication()
        authorization = ReadOnlyAuthorization()
        serializer = PrettyJSONSerializer()
        always_return_data = True  
        include_resource_uri = False      
        
class OrganisationResource(ModelResource):
    class Meta:
        queryset = Organisation.objects.all()
        resource_name = 'organisation'
        allowed_methods = ['get']
        fields = ['name', 'url', 'location']
        authentication = ApiKeyAuthentication()
        authorization = ReadOnlyAuthorization() 
        serializer = PrettyJSONSerializer()
        always_return_data = True 
        include_resource_uri = False
        
class ResourceFileResource(ModelResource):
    class Meta:
        queryset = ResourceFile.objects.all()
        resource_name = 'resourcefile'
        allowed_methods = ['get']
        fields = ['file', 'description']
        authentication = ApiKeyAuthentication()
        authorization = ReadOnlyAuthorization() 
        serializer = PrettyJSONSerializer()
        always_return_data = True 
        include_resource_uri = False
     
    def dehydrate_file(self,bundle):
        return get_full_url_prefix(bundle) + settings.MEDIA_URL + bundle.obj.file.name
        
class ResourceURLResource(ModelResource):
    class Meta:
        queryset = ResourceURL.objects.all()
        resource_name = 'resourceurl'
        allowed_methods = ['get']
        fields = ['url', 'description']
        authentication = ApiKeyAuthentication()
        authorization = ReadOnlyAuthorization() 
        serializer = PrettyJSONSerializer()
        always_return_data = True 
        include_resource_uri = False
        
        
class ResourceTagResource(ModelResource):
    tag = fields.ToOneField('mpowering.api.resources.TagResource', 'tag', full=True)
    class Meta:
        queryset = ResourceTag.objects.all()
        allowed_methods = ['get']
        include_resource_uri = False
        authentication = ApiKeyAuthentication()
        authorization = ReadOnlyAuthorization()
        serializer = PrettyJSONSerializer()
        always_return_data = True  
        include_resource_uri = False 
        
        
class TagResource(ModelResource):
    url = fields.CharField(readonly=True)
    class Meta:
        queryset = Tag.objects.all()
        resource_name = 'tag'
        allowed_methods = ['get']
        fields = ['name', 'image']
        authentication = ApiKeyAuthentication()
        authorization = ReadOnlyAuthorization() 
        serializer = PrettyJSONSerializer()
        always_return_data = True 
        include_resource_uri = False
        
    def dehydrate_url(self,bundle):
        url = get_full_url_prefix(bundle) + reverse('mpowering_tags', args=[bundle.obj.slug])
        return url
 
    def dehydrate_image(self,bundle):
        if bundle.obj.image != '':
            return get_full_url_prefix(bundle) + settings.MEDIA_URL + bundle.obj.image.name
        else:
            return None
 
 
 
# Helper methods.   
def get_full_url_prefix(bundle):
    if bundle.request.is_secure():
        prefix = 'https://'
    else:
        prefix = 'http://'
    if bundle.request.META['SERVER_PORT'] == 80 or bundle.request.META['SERVER_PORT'] == 443:
        port = ""
    else:
        port =  ":" + bundle.request.META['SERVER_PORT']
    return prefix + bundle.request.META['SERVER_NAME'] + port
    