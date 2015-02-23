
import datetime
from django.db.models import Count
from django.shortcuts import render,render_to_response
from django.template import RequestContext
from django.utils import timezone
from django.utils.translation import ugettext as _

from mpowering.analytics.models import UserLocationVisualization

from mpowering.models import SearchTracker

# Create your views here.


def home_view(request):
    start_date = timezone.now() - datetime.timedelta(days=31)
    popular_searches = SearchTracker.objects.filter(access_date__gte=start_date).values('query').annotate(total_hits=Count('id')).order_by('-total_hits')[:10]
    return render_to_response('mpowering/analytics/home.html',
                              {'popular_searches': popular_searches },
                              context_instance=RequestContext(request))
    
def map_view(request):
    
    return render_to_response('mpowering/analytics/map.html',
                              {},
                              context_instance=RequestContext(request))

# scan url

# pending CRT

# pending MEP

# map

# popular Searches

# 