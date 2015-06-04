
import datetime
import dateutil.relativedelta
import json
import tablib

from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.contrib.auth.models import User
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render,render_to_response
from django.template import RequestContext
from django.utils import timezone
from django.utils.translation import ugettext as _

from orb.analytics.models import UserLocationVisualization
from orb.models import Resource, SearchTracker, ResourceTracker, Tag, TagOwner, TagTracker

# Create your views here.

def home_view(request):
    if not request.user.is_staff:
        return HttpResponse(status=401,content="Not Authorized") 
    start_date = timezone.now() - datetime.timedelta(days=31)
    end_date = timezone.now()
    pending_crt_resources = Resource.objects.filter(status=Resource.PENDING_CRT).order_by('create_date')
    pending_mep_resources = Resource.objects.filter(status=Resource.PENDING_MRT).order_by('create_date')
    popular_searches = SearchTracker.objects.filter(access_date__gte=start_date).values('query').annotate(total_hits=Count('id')).order_by('-total_hits')[:10]
    popular_resources = ResourceTracker.objects.filter(access_date__gte=start_date).exclude(resource=None).values('resource','resource__slug','resource__title').annotate(total_hits=Count('id')).order_by('-total_hits')[:10]
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
    
    
    user_registrations = []
    no_days = (end_date-start_date).days + 1
    for i in range(0,no_days,+1):
        temp = start_date + datetime.timedelta(days=i)
        day = temp.strftime("%d")
        month = temp.strftime("%m")
        year = temp.strftime("%Y")
        no_registrations = User.objects.filter(date_joined__day=day,date_joined__month=month,date_joined__year=year).count()     
        user_registrations.append([temp.strftime("%d %b %y"),no_registrations])
    
    total_user_registrations = User.objects.exclude(is_staff=True).count(); 
    
    countries = UserLocationVisualization.objects.exclude(country_name='').values_list('country_name',flat=True).distinct().order_by('country_name')
    
    return render_to_response('orb/analytics/home.html',
                              {'pending_crt_resources': pending_crt_resources,
                               'pending_mep_resources': pending_mep_resources,
                               'popular_searches': popular_searches,
                               'popular_resources': popular_resources,
                               'organisations': organisations,
                               'recent_activity': recent_activity,
                               'searches_no_results': searches_no_results,
                               'user_registrations': user_registrations,
                               'total_user_registrations': total_user_registrations,
                               'countries': countries,
                                },
                              context_instance=RequestContext(request))
    
def map_view(request):
    if not request.user.is_staff:
        return HttpResponse(status=401,content="Not Authorized") 
    return render_to_response('orb/analytics/map.html',
                              {},
                              context_instance=RequestContext(request))


def visitor_view(request, year=None, month=None):
    if not request.user.is_staff:
        return HttpResponse(status=401,content="Not Authorized") 
    
    if year == None and month == None:
        today = timezone.now()
        last_month = today - dateutil.relativedelta.relativedelta(months=1)
    
        analytics_month = last_month.month
        analytics_year = last_month.year
    else:
        analytics_month = month
        analytics_year = year
    
    archive_month = datetime.datetime.strptime(str(analytics_year) +"-"+str(analytics_month)+ "-1", "%Y-%m-%d")
    
    # for last full month:
    
    stats = {}
    #  total unique users - and no hits
    #  unique loggedin users  - and no hits
    user_hits = list(ResourceTracker.objects.filter(access_date__month=analytics_month, access_date__year=analytics_year).exclude(user=None).values_list('user_id', flat=True).distinct())
    user_hits += list(TagTracker.objects.filter(access_date__month=analytics_month, access_date__year=analytics_year).exclude(user=None).values_list('user_id', flat=True).distinct())
    user_hits += list(SearchTracker.objects.filter(access_date__month=analytics_month, access_date__year=analytics_year).exclude(user=None).values_list('user_id', flat=True).distinct())

    stats['user_hits'] = len(set(user_hits))
    
    #  unique anon users (IP addess)  - and no hits
    anon_hits = list(ResourceTracker.objects.filter(access_date__month=analytics_month, access_date__year=analytics_year, user=None).values_list('ip', flat=True).distinct())
    anon_hits += list(TagTracker.objects.filter(access_date__month=analytics_month, access_date__year=analytics_year, user=None).values_list('ip', flat=True).distinct())
    anon_hits += list(SearchTracker.objects.filter(access_date__month=analytics_month, access_date__year=analytics_year, user=None).values_list('ip', flat=True).distinct())

    stats['anon_hits'] = len(set(anon_hits))
    
    #resources
    tz = timezone.get_default_timezone()
    last_day = datetime.datetime(int(analytics_year), int(analytics_month), 1, 23, 59, tzinfo=tz) + dateutil.relativedelta.relativedelta(day=1, months=+1, days=-1)
    stats['resources'] = Resource.objects.filter(create_date__lte=last_day,status=Resource.APPROVED).count()

    #searches
    stats['searches'] = SearchTracker.objects.filter(access_date__month=analytics_month, access_date__year=analytics_year).count()
    
    #users registered
    stats['registrations'] = User.objects.filter(date_joined__month=analytics_month, date_joined__year=analytics_year).count()
    
    #languages
    stats['languages'] = Tag.objects.filter(resourcetag__resource__status=Resource.APPROVED, resourcetag__resource__create_date__lte=last_day, category__slug='language').distinct().count()
    
    #locations/countries
    loc_hits = list(ResourceTracker.objects.filter(access_date__month=analytics_month, access_date__year=analytics_year).values_list('ip', flat=True).distinct())
    loc_hits += list(TagTracker.objects.filter(access_date__month=analytics_month, access_date__year=analytics_year).values_list('ip', flat=True).distinct())
    loc_hits += list(SearchTracker.objects.filter(access_date__month=analytics_month, access_date__year=analytics_year).values_list('ip', flat=True).distinct())

    countries = UserLocationVisualization.objects.filter(ip__in=loc_hits).values_list('country_code').distinct().count()
    stats['countries'] = countries
    
    # get links for previous months
    month_views = ResourceTracker.objects.all().datetimes('access_date','month','DESC')
    
    return render_to_response('orb/analytics/visitor.html',
                              {
                               'archive_month': archive_month,
                               'stats': stats,
                               'month_views': month_views,
                               },
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
    
    # get the monthly trackers
    export = ResourceTracker.objects.filter(resource__resourcetag__tag=tag,resource__status=Resource.APPROVED).datetimes('access_date','month','DESC')
    
    # get the resources
    resources = Resource.objects.filter(resourcetag__tag=tag).distinct().order_by('title')
    
    return render_to_response('orb/analytics/tag.html',
                              { 'tag': tag,
                               'recent_activity': recent_activity,
                               'page': trackers,
                               'export': export,
                               'resources': resources  },
                              context_instance=RequestContext(request))


def tag_download(request,id, year, month):
    if not is_tag_owner(request, id):
        return HttpResponse(status=401,content="Not Authorized")
    
    tag = Tag.objects.get(pk=id)
     
    headers = ('Date', 'Resource', 'Resource File or URL', 'IP Address', 'User Agent', 'Country', 'Lat', 'Lng', 'Location')
    data = []
    data = tablib.Dataset(*data, headers=headers)
    
    trackers = ResourceTracker.objects.filter(resource__resourcetag__tag=tag,
                                              resource__status=Resource.APPROVED,
                                              access_date__month=month, 
                                              access_date__year=year).order_by('access_date')
    
    for t in trackers:
        if t.resource.title:
            if t.resource_file and t.resource_file.filename():
                print t.resource_file.filename()
                object = t.resource_file.filename()
            elif t.resource_url and t.resource_url.url:
                object = t.resource_url.url
            else:
                object = "--"
                
            if t.get_location():
                lat = t.get_location().lat
                lng = t.get_location().lng
                location = t.get_location().region 
                country = t.get_location().country_name
            else:
                lat = ''
                lng = ''
                location = ''
                country = ''
            data.append(
                            (
                                t.access_date.strftime('%Y-%m-%d %H:%M:%S'), 
                                t.resource.title, 
                                object,
                                t.ip, 
                                t.user_agent, 
                                country ,
                                lat, 
                                lng, 
                                location 
                            )
                        )
       
            
    response = HttpResponse(data.xls, content_type='application/vnd.ms-excel;charset=utf-8')
    response['Content-Disposition'] = "attachment; filename=export-"+str(year)+ "-"+ str(month) +".xls"

    return response

def mailing_list_view(request):
    if not request.user.is_staff:
        return HttpResponse(status=401,content="Not Authorized")
    
    users = User.objects.filter(userprofile__mailing=True).order_by('first_name')
     
    headers = ('Date joined', 'First name', 'Last name', 'Organisation', 'Role', 'Email')
    data = []
    data = tablib.Dataset(*data, headers=headers)

    
    for u in users:
        
        if u.userprofile.role:
            role = u.userprofile.role.name
        else:
            role = u.userprofile.role_other
            
        if u.userprofile.organisation:
            org = u.userprofile.organisation.name
        else:
            org = ''
        data.append(
                    (
                        u.date_joined.strftime('%Y-%m-%d %H:%M:%S'), 
                        u.first_name, 
                        u.last_name, 
                        org, 
                        role,
                        u.email    
                    )
                )
       
            
    response = HttpResponse(data.xls, content_type='application/vnd.ms-excel;charset=utf-8')
    response['Content-Disposition'] = "attachment; filename=orb-mailing-list-" + timezone.now().strftime('%Y-%m-%d') +".xls"

    return response
    
# Helper functions
def is_tag_owner(request,id):
    if not request.user.is_authenticated:
        return False
    
    if request.user.is_staff:
        return True
    
    try:
        TagOwner.objects.get(tag__pk=id,user__id=request.user.id)
        return True
    except TagOwner.DoesNotExist:
        return False