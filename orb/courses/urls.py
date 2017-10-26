from django.conf.urls import url
from orb.courses import views


urlpatterns = [
    url(r'^$', view=views.course_list, name="courses_list"),
    url(r'^new/$', view=views.CourseCreateView.as_view(), name="courses_create"),
    url(r'^(?P<pk>\d+)/$', view=views.CourseView.as_view(), name="courses_edit"),
    url(r'^(?P<pk>\d+)\.mbz$', view=views.ExportView.as_view(), name="courses_moodle_export"),
]
