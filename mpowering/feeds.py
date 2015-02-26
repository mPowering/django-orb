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
        return Resource.objects.all()[:20]