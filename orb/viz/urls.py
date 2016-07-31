from django.conf.urls import patterns
from django.conf.urls import url


urlpatterns = [
    url(r'^country/$', 'orb.viz.views.country_map_view', name="orb_country_map"),
]
