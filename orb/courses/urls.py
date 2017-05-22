from django.conf.urls import url
from orb.courses import views


urlpatterns = [
    url(r'^$', view=views.course_list, name="courses_list"),
    url(r'^new/$', view=views.course_create, name="courses_create"),
    url(r'^(?P<pk>\d+)/$', view=views.CourseUpdateView.as_view(), name="courses_edit"),
]
