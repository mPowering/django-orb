from django.conf.urls import url


urlpatterns = [
    url(r'^$', 'orb.toolkits.views.toolkit_home_view', name="orb_toolkits_home"),
]
