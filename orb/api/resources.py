
import json
import re

from django.conf import settings
from django.core.paginator import Paginator, InvalidPage
from django.core.urlresolvers import reverse
from django.conf.urls import url
from django.http import HttpRequest, HttpResponse
from django.http.response import Http404
from django.utils.translation import ugettext as _

from haystack.query import SearchQuerySet

from orb.api.authorization import ORBResourceAuthorization, ORBAuthorization
from orb.api.error_codes import *
from orb.api.exceptions import ORBAPIBadRequest
from orb.api.serializers import PrettyJSONSerializer, ResourceSerializer
from orb.models import Resource, ResourceFile, ResourceURL, ResourceTag
from orb.models import User, Tag, Category, ResourceTracker, SearchTracker
from orb.signals import resource_viewed, search
from orb.views import resource_can_edit

from tastypie import fields
from tastypie.authentication import Authentication,ApiKeyAuthentication
from tastypie.authorization import ReadOnlyAuthorization, Authorization
from tastypie.exceptions import BadRequest, Unauthorized
from tastypie.models import ApiKey
from tastypie.resources import ModelResource
from tastypie.throttle import CacheDBThrottle
from tastypie.utils import trailing_slash


class ResourceResource(ModelResource):
    '''
    To get, post and pushing resources
    '''
    files = fields.ToManyField('orb.api.resources.ResourceFileResource', 'resourcefile_set', related_name='resource', full=True, null = True)
    urls = fields.ToManyField('orb.api.resources.ResourceURLResource', 'resourceurl_set', related_name='resource', full=True, null = True)
    tags = fields.ToManyField('orb.api.resources.ResourceTagResource', 'resourcetag_set', related_name='resource', full=True, null = True)
    url = fields.CharField(readonly=True)
    
    class Meta:
        queryset = Resource.objects.all()
        resource_name = 'resource'
        allowed_methods = ['get','post']
        authentication = ApiKeyAuthentication()
        authorization = ORBResourceAuthorization() 
        serializer = ResourceSerializer()
        always_return_data = True 
        include_resource_uri = True
        throttle = CacheDBThrottle(throttle_at=150, timeframe=3600)

    def dehydrate_image(self,bundle):
        if bundle.obj.image:
            return get_full_url_prefix(bundle) + settings.MEDIA_URL + bundle.obj.image.name
        else:
            return None
    
    def dehydrate_url(self,bundle):
        url = get_full_url_prefix(bundle) + reverse('orb_resource', args=[bundle.obj.slug])
        return url
    
    def authorized_read_detail(self, object_list, bundle):
        # add to ResourceTracker
        if bundle.obj.id:
            resource_viewed.send(sender=bundle.obj, resource=bundle.obj, request=bundle.request, type=ResourceTracker.VIEW_API)
    
    def prepend_urls(self):
        '''
        for implementing a search API
        '''
        return [
            url(r"^(?P<resource_name>%s)/search%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('get_search'), name="api_get_search"),
        ]
        
    def get_search(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        self.is_authenticated(request)
        self.throttle_check(request)

        if request.GET.get('q', '') == '':
            raise ORBAPIBadRequest(ERROR_CODE_SEARCH_NO_QUERY)
        
        # Do the query.
        sqs = SearchQuerySet().models(Resource).load_all().auto_query(request.GET.get('q', ''))
        paginator = Paginator(sqs, 20)

        
        try:
            page = paginator.page(int(request.GET.get('page', 1)))
        except InvalidPage:
            raise Http404("Sorry, no results on that page.")

        objects = []

        for result in page.object_list:
            if result:
                bundle = self.build_bundle(obj=result.object, request=request)
                bundle = self.full_dehydrate(bundle)
                objects.append(bundle)

        object_list = {
            'objects': objects,
        }
        
        tracker = SearchTracker()
        if not request.user.is_anonymous():
            tracker.user = request.user
        tracker.query = request.GET.get('q', '')
        tracker.no_results = sqs.count()
        tracker.ip = request.META.get('REMOTE_ADDR','0.0.0.0')
        tracker.user_agent = request.META.get('HTTP_USER_AGENT','unknown')
        tracker.type = SearchTracker.SEARCH_API
        tracker.save()
        
        self.log_throttled_access(request)
        return self.create_response(request, object_list)    
       
    def hydrate(self, bundle, request=None):
        bundle.obj.create_user_id = bundle.request.user.id
        bundle.obj.update_user_id = bundle.request.user.id
        
        # check required fields
        if 'title' not in bundle.data or bundle.data['title'].strip() == '':
            raise ORBAPIBadRequest(ERROR_CODE_RESOURCE_NO_TITLE)

        if 'description' not in bundle.data or bundle.data['description'].strip() == '':
            raise ORBAPIBadRequest(ERROR_CODE_RESOURCE_NO_DESCRIPTION)

        # check that resource doesn't already exist for this user
        try:
            resource = Resource.objects.get(create_user=bundle.request.user,title =bundle.data['title'])
            rr = ResourceResource()
            bundle = rr.build_bundle(obj=resource,request=request)
            raise ORBAPIBadRequest(ERROR_CODE_RESOURCE_EXISTS,pk=resource.id)
        except Resource.DoesNotExist:
            pass
        
        return bundle
         
class ResourceFileResource(ModelResource):
    class Meta:
        queryset = ResourceFile.objects.all()
        resource_name = 'resourcefile'
        allowed_methods = ['get','delete']
        fields = ['id', 'file', 'title', 'description', 'order_by', 'file_size']
        authentication = ApiKeyAuthentication()
        authorization = ORBAuthorization() 
        serializer = PrettyJSONSerializer()
        always_return_data = True 
        include_resource_uri = True
        
    def dehydrate_file(self,bundle):
        if bundle.obj.file:
            return get_full_url_prefix(bundle) + settings.MEDIA_URL + bundle.obj.file.name
        else:
            return None
        
class ResourceURLResource(ModelResource):
    class Meta:
        queryset = ResourceURL.objects.all()
        resource_name = 'resourceurl'
        allowed_methods = ['get','post','delete']
        fields = ['id', 'url', 'title', 'description', 'order_by', 'file_size']
        authentication = ApiKeyAuthentication()
        authorization = ORBAuthorization() 
        serializer = PrettyJSONSerializer()
        always_return_data = True 
        include_resource_uri = True
     
    def hydrate(self, bundle, request=None):
        # check that user has permissions on the resource
        resource = Resource.objects.get(pk=bundle.data['resource_id'])
        user = User.objects.get(pk=bundle.request.user.id)
        if not resource_can_edit(resource, user):
            raise Unauthorized("You do not have edit access for this resource")
        
        bundle.obj.create_user_id = bundle.request.user.id  
        bundle.obj.update_user_id = bundle.request.user.id 
        bundle.obj.resource_id = bundle.data['resource_id']
        
        if 'file_size' not in bundle.data:
            bundle.obj.file_size = 0
            
        return bundle   
        
class ResourceTagResource(ModelResource):
    tag = fields.ToOneField('orb.api.resources.TagResource', 'tag', full=True)
    class Meta:
        queryset = ResourceTag.objects.all()
        resource_name = 'resourcetag'
        allowed_methods = ['get','post','delete']
        include_resource_uri = False
        authentication = ApiKeyAuthentication()
        authorization = ORBAuthorization()
        serializer = PrettyJSONSerializer()
        always_return_data = True  
        include_resource_uri = True
    
    def hydrate(self, bundle, request=None):
        
        if 'resource_id' not in bundle.data or not bundle.data['resource_id']:
            raise ORBAPIBadRequest(ERROR_CODE_RESOURCETAG_NO_RESOURCE)

        if 'tag_id' not in bundle.data or not bundle.data['tag_id']:
            raise ORBAPIBadRequest(ERROR_CODE_RESOURCETAG_NO_TAG)
        
        # check resource exists
        try:
            resource = Resource.objects.get(pk=bundle.data['resource_id'])
        except Resource.DoesNotExist:
            raise ORBAPIBadRequest(ERROR_CODE_RESOURCE_DOES_NOT_EXIST)
        
        # check tag exists
        try:
            tag = Tag.objects.get(pk=bundle.data['tag_id'])
        except Tag.DoesNotExist:
            raise ORBAPIBadRequest(ERROR_CODE_TAG_DOES_NOT_EXIST)
        
        # check that user has permissions on the resource
        user = User.objects.get(pk=bundle.request.user.id)
        if not resource_can_edit(resource, user):
            raise Unauthorized("You do not have edit access for this resource")
        
        # check that tag not already added to resource
        resource_tags = ResourceTag.objects.filter(resource=resource, tag=tag).count()
        if resource_tags != 0:
            raise ORBAPIBadRequest(ERROR_CODE_RESOURCETAG_EXISTS)
        
        bundle.obj.create_user_id = bundle.request.user.id  
        bundle.obj.resource_id = bundle.data['resource_id']
        bundle.obj.tag_id = bundle.data['tag_id']
        return bundle  
        
class TagResource(ModelResource):
    url = fields.CharField(readonly=True)
    class Meta:
        queryset = Tag.objects.all()
        resource_name = 'tag'
        allowed_methods = ['get','post']
        fields = ['id','name', 'image']
        filtering = {"name": [ "exact" ]}
        authentication = ApiKeyAuthentication()
        authorization = ORBAuthorization() 
        serializer = PrettyJSONSerializer()
        always_return_data = True 
        include_resource_uri = True
   
    def dehydrate_url(self,bundle):
        url = get_full_url_prefix(bundle) + reverse('orb_tags', args=[bundle.obj.slug])
        return url
 
    def dehydrate_image(self,bundle):
        if bundle.obj.image:
            return get_full_url_prefix(bundle) + settings.MEDIA_URL + bundle.obj.image.name
        else:
            return None
    
    def hydrate(self, bundle, request=None):
        
        # check not empty
        if bundle.data['name'].strip() == '':
            raise ORBAPIBadRequest(ERROR_CODE_TAG_EMPTY)
        
        # check not all non-word chars
        regex = re.compile('[,\.!?"\']')
        if regex.sub('', bundle.data['name'].strip()) == '':
            raise ORBAPIBadRequest(ERROR_CODE_TAG_EMPTY)
        
        # check tag doesn't already exist
        try:
            tag = Tag.objects.get(name=bundle.data['name'])
            tr = TagResource()
            bundle = tr.build_bundle(obj=tag,request=request)
            raise ORBAPIBadRequest(ERROR_CODE_TAG_EXISTS)
        except Tag.DoesNotExist:
            pass
        
        category = Category.objects.get(slug='other')
        bundle.obj.create_user_id = bundle.request.user.id  
        bundle.obj.update_user_id = bundle.request.user.id
        bundle.obj.category_id = category.id
        return bundle  
    
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
    