from django.conf.urls import url
from orb.review.views import (review_resource, resource_review_list, reject_resource,
                             assign_review, delete_resource)


urlpatterns = [
    url(r'^(?P<resource_id>\d+)/assignment/$',
        view=assign_review, name="orb_assign_review"),
    url(r'^(?P<resource_id>\d+)/delete/$',
        view=delete_resource, name="orb_delete_resource"),
    url(r'^(?P<resource_id>\d+)/assignment/(?P<review_id>\d+)/$',
        view=review_resource, name="orb_resource_review"),
    url(r'^(?P<resource_id>\d+)/assignment/(?P<review_id>\d+)/reject/$',
        view=reject_resource, name="orb_reject_resource"),
    url(r'^$', view=resource_review_list, name="orb_pending_resources"),
]