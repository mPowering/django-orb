from django.conf.urls import url

from orb.viz import views

urlpatterns = [
    url(r'^country/$', views.country_map_view, name="orb_country_map"),
]
