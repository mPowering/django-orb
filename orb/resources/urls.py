from django.conf.urls import url
from orb.resources.views import review_resource, resource_review_list


urlpatterns = [
    url(r'^(?P<resource_id>\d+)/review/(?P<review_id>\d+)/$',
        view=review_resource, name="orb_resource_review"),
    url(r'^pending/$', view=resource_review_list, name="orb_pending_resources"),
]
