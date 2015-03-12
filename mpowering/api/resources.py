
from django.conf import settings
from django.core.paginator import Paginator, InvalidPage
from django.core.urlresolvers import reverse
from django.conf.urls import url
from django.utils.translation import ugettext as _

from haystack.query import SearchQuerySet

from mpowering.api.serializers import PrettyJSONSerializer, ResourceSerializer
from mpowering.models import Resource, ResourceFile, ResourceURL, ResourceTag
from mpowering.models import User, Tag, Category, ResourceTracker, SearchTracker
from mpowering.signals import resource_viewed, search

from tastypie import fields
from tastypie.authentication import Authentication,ApiKeyAuthentication
from tastypie.authorization import ReadOnlyAuthorization, Authorization
from tastypie.exceptions import BadRequest
from tastypie.models import ApiKey
from tastypie.resources import ModelResource
from tastypie.throttle import CacheDBThrottle
from tastypie.utils import trailing_slash



class ResourceResource(ModelResource):
    files = fields.ToManyField('mpowering.api.resources.ResourceFileResource', 'resourcefile_set', related_name='resource', full=True, null = True)
    urls = fields.ToManyField('mpowering.api.resources.ResourceURLResource', 'resourceurl_set', related_name='resource', full=True, null = True)
    tags = fields.ToManyField('mpowering.api.resources.ResourceTagResource', 'resourcetag_set', related_name='resource', full=True, null = True)
    url = fields.CharField(readonly=True)
    
    class Meta:
        queryset = Resource.objects.filter(status=Resource.APPROVED)
        resource_name = 'resource'
        allowed_methods = ['get','post']
        authentication = ApiKeyAuthentication()
        authorization = Authorization() 
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
        url = get_full_url_prefix(bundle) + reverse('mpowering_resource', args=[bundle.obj.slug])
        return url
    
    def authorized_read_detail(self, object_list, bundle):
        # add to ResourceTracker
        resource_viewed.send(sender=bundle.obj, resource=bundle.obj, request=bundle.request, type=ResourceTracker.VIEW_API)
    
    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/search%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('get_search'), name="api_get_search"),
        ]
        
    def get_search(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        self.is_authenticated(request)
        self.throttle_check(request)

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
    
        # add to ResourceTracker
        #search.send(sender=sqs, query=request.GET.get('q', ''), no_results=sqs.count(),  request=request, type=SearchTracker.VIEW_API)
        
        self.log_throttled_access(request)
        return self.create_response(request, object_list)    
       
    def hydrate(self, bundle, request=None):
        bundle.obj.create_user_id = bundle.request.user.id
        bundle.obj.update_user_id = bundle.request.user.id
        # check required fields
        if 'title' not in bundle.data:
            raise BadRequest(_(u'No title provided'))
        
        if 'description' not in bundle.data:
            raise BadRequest(_(u'No description provided'))
        
        # check that resource doesn't already exist for this user
        try:
            Resource.objects.get(create_user=bundle.request.user,title =bundle.data['title'] )
            raise BadRequest(_(u'You have already uploaded a resource with this title'))
        except Resource.DoesNotExist:
            pass
        
        return bundle
         
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
        if bundle.obj.file:
            return get_full_url_prefix(bundle) + settings.MEDIA_URL + bundle.obj.file.name
        else:
            return None
        
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
        if bundle.obj.image:
            return get_full_url_prefix(bundle) + settings.MEDIA_URL + bundle.obj.image.name
        else:
            return None
     
    def hydrate(self, bundle, request=None):
        
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
    