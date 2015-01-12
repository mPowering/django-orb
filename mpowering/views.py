
from django.shortcuts import render,render_to_response
from django.template import RequestContext

from mpowering.models import Tag, Resource

# Create your views here.


def home_view(request):
    topics = Tag.objects.filter(category__slug='health-topic').order_by('order_by')
    return render_to_response('mpowering/home.html',
                              {'topics': topics,},
                              context_instance=RequestContext(request))

def tag_view(request,tag_slug):
    tag = Tag.objects.get(slug=tag_slug)
    resources = Resource.objects.filter(resourcetag__tag=tag)
    return render_to_response('mpowering/tag.html',
                              {'resources': resources,
                               'tag': tag, },
                              context_instance=RequestContext(request))
    