from django.conf.urls import patterns
from django.conf.urls import url


urlpatterns = patterns('',
    url(r'^$', 'orb.toolkits.views.toolkit_home_view', name="orb_toolkits_home"),
)
