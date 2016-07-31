from django.conf.urls import url


urlpatterns = [
    url(r'^$', 'orb.rating.views.resource_rate_view', name="orb_rate"),
]
