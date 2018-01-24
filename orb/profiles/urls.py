from django.conf.urls import url
from django.views.generic import TemplateView

from orb.profiles import views

urlpatterns = [
    url(r'^register/$', view=views.RegistrationView.as_view(), name="profile_register"),
    url(r'^register/thanks/$', TemplateView.as_view(template_name="orb/thanks.html"), name="profile_register_thanks"),
    url(r'^login/$', 'orb.profiles.views.login_view', name="profile_login"),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'template_name': 'orb/logout.html'}, name="profile_logout"),
    url(r'^setlang/$', 'django.views.i18n.set_language', name="profile_set_language"),
    url(r'^reset/$', 'orb.profiles.views.reset', name="profile_reset"),
    url(r'^reset/sent/$', TemplateView.as_view(template_name="orb/profile/reset-sent.html"), name="profile_reset_sent"),
    url(r'^view/(?P<id>\d+)/$', 'orb.profiles.views.view_profile', name="profile_view"),
    url(r'^edit/$', 'orb.profiles.views.edit', name="my_profile_edit"),
    url(r'^view/$', 'orb.profiles.views.view_my_profile', name="my_profile_view"),
    url(r'^view/bookmarks/$', 'orb.profiles.views.view_my_bookmarks', name="my_bookmarks_view"),
    url(r'^view/ratings/$', 'orb.profiles.views.view_my_ratings', name="my_ratings_view"),
]
