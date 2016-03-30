"""
 Script to get user locations based on their IP address in the Tracker model
 
 For full instructions, see the documentation at 
 https://oppiamobile.readthedocs.org/en/latest/
"""

import time
import urllib2
import json
from django.db.models import Count
from orb.models import ResourceTracker, SearchTracker, TagTracker
from orb.analytics.models import UserLocationVisualization


def run():
    tracker_ip_hits = ResourceTracker.objects.all().values(
        'ip').annotate(count_hits=Count('ip'))

    for t in tracker_ip_hits:
        # lookup whether already cached in db
        try:
            cached = UserLocationVisualization.objects.get(
                ip=t['ip'], source='resource')
            cached.hits = t['count_hits']
            cached.save()
            print "resource hits updated"
        except UserLocationVisualization.DoesNotExist:
            update_via_freegeoip(t, 'resource')

    search_ip_hits = SearchTracker.objects.all().values(
        'ip').annotate(count_hits=Count('ip'))
    for s in search_ip_hits:
        # lookup whether already cached in db
        try:
            cached = UserLocationVisualization.objects.get(
                ip=s['ip'], source='search')
            cached.hits = s['count_hits']
            cached.save()
            print "search hits updated"
        except UserLocationVisualization.DoesNotExist:
            update_via_freegeoip(s, 'search')

    tag_ip_hits = TagTracker.objects.all().values(
        'ip').annotate(count_hits=Count('ip'))
    for t in tag_ip_hits:
        # lookup whether already cached in db
        try:
            cached = UserLocationVisualization.objects.get(
                ip=t['ip'], source='tag')
            cached.hits = t['count_hits']
            cached.save()
            print "tag hits updated"
        except UserLocationVisualization.DoesNotExist:
            update_via_freegeoip(t, 'tag')


def update_via_freegeoip(t, source):
    url = 'https://freegeoip.net/json/%s' % (t['ip'])
    print t['ip'] + " : " + url
    try:
        u = urllib2.urlopen(urllib2.Request(url), timeout=10)
        data = u.read()
        dataJSON = json.loads(data, "utf-8")
        print dataJSON
    except:
        return

    try:
        if dataJSON['latitude'] != 0 and dataJSON['longitude'] != 0:
            viz = UserLocationVisualization()
            viz.ip = t['ip']
            viz.lat = dataJSON['latitude']
            viz.lng = dataJSON['longitude']
            viz.hits = t['count_hits']
            viz.region = dataJSON['city'] + " " + dataJSON['region_name']
            viz.country_code = dataJSON['country_code']
            viz.country_name = dataJSON['country_name']
            viz.geonames_data = dataJSON
            viz.source = source
            viz.save()
    except:
        pass
    time.sleep(1)


if __name__ == "__main__":
    import django
    django.setup()
    run()
