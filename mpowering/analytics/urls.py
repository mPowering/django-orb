# mpowering/urls.py
from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

urlpatterns = patterns('',

    url(r'^$', 'mpowering.analytics.views.home_view', name="mpowering_analytics_home"),

)
