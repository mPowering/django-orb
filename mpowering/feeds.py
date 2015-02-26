from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from mpowering.models import Resource, Tag

class LatestEntries(Feed):
    description_template = 'feeds/resource.html'
    
    def get_object(self, request, tag_slug):
        return get_object_or_404(Tag, slug=tag_slug)

    def title(self, obj):
        return "mPowering resources tagged with %s" % obj.name

    def link(self, obj):
        return ""

    def description(self, obj):
        return "Resources recently tagged with  %s" % obj.name

    def items(self, obj):
        return Resource.objects.filter(status=Resource.APPROVED, resourcetag__tag=obj).order_by('-create_date')[:20]
    
    def item_pubdate(self, item):
        return item.create_date
    
    def item_updateddate(self, item):
        return item.update_date