from django.conf.urls import url
from orb.review.views import (review_resource, resource_review_list, reject_resource,
                                 assign_review)


urlpatterns = [
    url(r'^(?P<resource_id>\d+)/review/$', view=assign_review, name="orb_assign_review"),
    url(r'^(?P<resource_id>\d+)/review/(?P<review_id>\d+)/$',
        view=review_resource, name="orb_resource_review"),
    url(r'^(?P<resource_id>\d+)/review/(?P<review_id>\d+)/reject/$',
        view=reject_resource, name="orb_reject_resource"),
    url(r'^pending/$', view=resource_review_list, name="orb_pending_resources"),
]