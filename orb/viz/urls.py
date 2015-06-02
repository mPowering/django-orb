# orb/viz/urls.py
from django.conf import settings
from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView


urlpatterns = patterns('',
    
    
    url(r'^$', 'orb.viz.views.country_map_view', name="orb_country_map"),
    
)
