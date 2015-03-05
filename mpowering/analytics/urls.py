# mpowering/urls.py
from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

urlpatterns = patterns('',

    url(r'^$', 'mpowering.analytics.views.home_view', name="mpowering_analytics_home"),
    url(r'^map/$', 'mpowering.analytics.views.map_view', name="mpowering_analytics_map"),
    url(r'^organisation/(?P<id>\d+)/$', 'mpowering.analytics.views.org_view', name="mpowering_analytics_org"),

)
