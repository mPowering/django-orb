# mpowering/urls.py
from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

urlpatterns = patterns('',

    url(r'^$', 'mpowering.analytics.views.home_view', name="mpowering_analytics_home"),
    url(r'^map/$', 'mpowering.analytics.views.map_view', name="mpowering_analytics_map"),
    url(r'^tag/(?P<id>\d+)/$', 'mpowering.analytics.views.tag_view', name="mpowering_analytics_tag"),
    url(r'^tag/(?P<id>\d+)/download/(?P<year>\d+)/(?P<month>\d+)/$', 'mpowering.analytics.views.tag_download', name="mpowering_analytics_download"),

)
