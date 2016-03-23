from django.conf.urls import patterns
from django.conf.urls import url


urlpatterns = patterns('',
    url(r'^$', 'orb.rating.views.resource_rate_view', name="orb_rate"),
)
