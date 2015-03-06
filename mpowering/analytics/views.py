
import datetime

from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render,render_to_response
from django.template import RequestContext
from django.utils import timezone
from django.utils.translation import ugettext as _

from mpowering.analytics.models import UserLocationVisualization

from mpowering.models import Resource, SearchTracker, ResourceTracker, Tag

# Create your views here.


def home_view(request):
    if not request.user.is_staff:
        return HttpResponse(status=401,content="Not Authorized") 
    start_date = timezone.now() - datetime.timedelta(days=31)
    popular_searches = SearchTracker.objects.filter(access_date__gte=start_date).values('query').annotate(total_hits=Count('id')).order_by('-total_hits')[:10]
    popular_resources = ResourceTracker.objects.filter(access_date__gte=start_date).values('resource','resource__slug','resource__title').annotate(total_hits=Count('id')).order_by('-total_hits')[:10]
    organisations = Tag.objects.filter(category__slug='organisation').distinct().order_by('name')
    
    return render_to_response('mpowering/analytics/home.html',
                              {'popular_searches': popular_searches,
                               'popular_resources': popular_resources,
                               'organisations': organisations},
                              context_instance=RequestContext(request))
    
def map_view(request):
    if not request.user.is_staff:
        return HttpResponse(status=401,content="Not Authorized") 
    return render_to_response('mpowering/analytics/map.html',
                              {},
                              context_instance=RequestContext(request))


def org_view(request, id):
    if not request.user.is_staff:
        return HttpResponse(status=401,content="Not Authorized") 
    
    organisation = Tag.objects.get(pk=id, category__slug='organisation')
    start_date = timezone.now() - datetime.timedelta(days=31)
    trackers = ResourceTracker.objects.filter(access_date__gte=start_date,resource__resourcetag__tag=organisation,resource__status=Resource.APPROVED).order_by('-access_date')
    
    paginator = Paginator(trackers, 20)
    # Make sure page request is an int. If not, deliver first page.
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    
    try:
        trackers = paginator.page(page)
    except (EmptyPage, InvalidPage):
        trackers = paginator.page(paginator.num_pages)
    
    return render_to_response('mpowering/analytics/organisation.html',
                              {
                               'organisation': organisation,
                               'page':trackers,},
                              context_instance=RequestContext(request))
    
# scan url

# pending CRT

# pending MEP

# map

# 