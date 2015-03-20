
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
    end_date = timezone.now()
    pending_crt_resources = Resource.objects.filter(status=Resource.PENDING_CRT)
    pending_mep_resources = Resource.objects.filter(status=Resource.PENDING_MRT)
    popular_searches = SearchTracker.objects.filter(access_date__gte=start_date).values('query').annotate(total_hits=Count('id')).order_by('-total_hits')[:10]
    popular_resources = ResourceTracker.objects.filter(access_date__gte=start_date).values('resource','resource__slug','resource__title').annotate(total_hits=Count('id')).order_by('-total_hits')[:10]
    organisations = Tag.objects.filter(category__slug='organisation',resourcetag__isnull=False).annotate(total_resources=Count('resourcetag__id')).order_by('name')
    
    snor = timezone.now() - datetime.timedelta(days=90)
    searches_no_results = SearchTracker.objects.filter(access_date__gte=snor, no_results=0).values('query').annotate(total_hits=Count('id')).order_by('-total_hits')[:10]
    
    recent_activity = []
    no_days = (end_date-start_date).days + 1
    for i in range(0,no_days,+1):
        temp = start_date + datetime.timedelta(days=i)
        day = temp.strftime("%d")
        month = temp.strftime("%m")
        year = temp.strftime("%Y")
        r_trackers = ResourceTracker.objects.filter(access_date__day=day,access_date__month=month,access_date__year=year)
        s_trackers = SearchTracker.objects.filter(access_date__day=day,access_date__month=month,access_date__year=year)
        count_activity = {'resource':0, 'resource_file':0, 'resource_url':0, 'search':0, 'total':0}
        for r in r_trackers:
            count_activity['total']+=1
            if r.resource_file:
                count_activity['resource_file']+=1
            elif r.resource_url:
                count_activity['resource_url']+=1
            else:
                count_activity['resource']+=1
        for s in s_trackers:
            count_activity['total']+=1
            count_activity['search']+=1
            
        recent_activity.append([temp.strftime("%d %b %y"),count_activity])
        
    return render_to_response('mpowering/analytics/home.html',
                              {'pending_crt_resources': pending_crt_resources,
                               'pending_mep_resources': pending_mep_resources,
                               'popular_searches': popular_searches,
                               'popular_resources': popular_resources,
                               'organisations': organisations,
                               'recent_activity': recent_activity,
                               'searches_no_results': searches_no_results},
                              context_instance=RequestContext(request))
    
def map_view(request):
    if not request.user.is_staff:
        return HttpResponse(status=401,content="Not Authorized") 
    return render_to_response('mpowering/analytics/map.html',
                              {},
                              context_instance=RequestContext(request))


def tag_view(request,id):
    if not is_tag_owner(request, id):
        return HttpResponse(status=401,content="Not Authorized")
    
    tag = Tag.objects.get(pk=id) 
    
    start_date = timezone.now() - datetime.timedelta(days=31)
    end_date = timezone.now()
    
    # Activity Graph
    recent_activity = []
    no_days = (end_date-start_date).days + 1
    for i in range(0,no_days,+1):
        temp = start_date + datetime.timedelta(days=i)
        day = temp.strftime("%d")
        month = temp.strftime("%m")
        year = temp.strftime("%Y")
        r_trackers = ResourceTracker.objects.filter(access_date__day=day,access_date__month=month,access_date__year=year, resource__resourcetag__tag=tag,resource__status=Resource.APPROVED)
        count_activity = {'resource':0, 'resource_file':0, 'resource_url':0, 'total':0}
        for r in r_trackers:
            count_activity['total']+=1
            if r.resource_file:
                count_activity['resource_file']+=1
            elif r.resource_url:
                count_activity['resource_url']+=1
            else:
                count_activity['resource']+=1
            
        recent_activity.append([temp.strftime("%d %b %y"),count_activity])
    
    
    # Activity detail
    trackers = ResourceTracker.objects.filter(access_date__gte=start_date,resource__resourcetag__tag=tag,resource__status=Resource.APPROVED).order_by('-access_date')
    
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
    
    return render_to_response('mpowering/analytics/tag.html',
                              { 'tag': tag,
                               'recent_activity': recent_activity,
                               'page':trackers,},
                              context_instance=RequestContext(request))

# Helper functions
def is_tag_owner(request,id):
    if not request.user.is_authenticated:
        return False
    
    if request.user.is_staff:
        return True
    try:
        tag_owner = TagOwner.objects.get(tag__pk=id,user=request.user)
        return True
    except TagOwner.DoesNotExist:
        return False