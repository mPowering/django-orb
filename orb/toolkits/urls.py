from django.conf.urls import url

from orb.toolkits import views

urlpatterns = [
    url(r'^$', view=views.ToolkitsView.as_view(), name="orb_toolkits"),
]
