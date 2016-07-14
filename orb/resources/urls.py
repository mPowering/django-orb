from django.conf.urls import url
from orb.resources.views import review_resource


urlpatterns = [
    url(r'^(?P<resource_id>\d+)/review/(?P<review_id>\d+)/$',
        view=review_resource, name="orb_resource_review"),
]
