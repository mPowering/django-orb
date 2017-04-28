from django.conf.urls import patterns
from django.conf.urls import url

urlpatterns = [
    url(r'^$', 'orb.analytics.views.home_view', name="orb_analytics_home"),
    url(r'^mailinglist/$', 'orb.analytics.views.mailing_list_view', name="orb_analytics_mailing_list"),
    url(r'^visitor/$', 'orb.analytics.views.visitor_view', name="orb_analytics_visitor"),
    url(r'^visitor/(?P<year>\d+)/(?P<month>\d+)/$', 'orb.analytics.views.visitor_view', name="orb_analytics_visitor_month_view"),
    url(r'^map/$', 'orb.analytics.views.map_view', name="orb_analytics_map"),
    url(r'^tag/(?P<id>\d+)/$', 'orb.analytics.views.tag_view', name="orb_analytics_tag"),
    url(r'^tag/(?P<id>\d+)/download/(?P<year>\d+)/(?P<month>\d+)/$', 'orb.analytics.views.tag_download', name="orb_analytics_download"),
    url(r'^resource/(?P<id>\d+)/$', 'orb.analytics.views.resource_view', name="orb_analytics_resource"),
]
