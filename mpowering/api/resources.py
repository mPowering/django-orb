
from tastypie import fields
from tastypie.authentication import Authentication,ApiKeyAuthentication
from tastypie.authorization import ReadOnlyAuthorization
from tastypie.models import ApiKey
from tastypie.resources import ModelResource

from mpowering.api.serializers import PrettyJSONSerializer, ResourceSerializer
from mpowering.models import Resource, ResourceOrganisation, Organisation

class ResourceResource(ModelResource):
    organisations = fields.ToManyField('mpowering.api.resources.ResourceOrganisationResource', 'resourceorganisation_set', related_name='resource', full=True)
    
    class Meta:
        queryset = Resource.objects.filter(status=Resource.APPROVED)
        resource_name = 'resource'
        allowed_methods = ['get']
        authentication = ApiKeyAuthentication()
        authorization = ReadOnlyAuthorization() 
        serializer = ResourceSerializer()
        always_return_data = True 
        include_resource_uri = True

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