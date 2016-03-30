from django.conf.urls import patterns
from django.conf.urls import url


urlpatterns = patterns('',
    url(r'^$', 'orb.bookmark.views.resource_bookmark_view', name="orb_bookmark"),
    url(r'^remove/(?P<resource_id>\d+)/$', 'orb.bookmark.views.resource_bookmark_remove_view', name="orb_bookmark_remove"),
)
