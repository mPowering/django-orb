# mpowering/profile/urls.py
from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

urlpatterns = patterns('',

    url(r'^register/$', 'mpowering.profile.views.register', name="profile_register"),
    url(r'^register/thanks/$', TemplateView.as_view(template_name="mpowering/thanks.html"), name="profile_register_thanks"),
    url(r'^login/$', 'mpowering.profile.views.login_view', name="profile_login"),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'template_name': 'mpowering/logout.html',}),
    url(r'^setlang/$', 'django.views.i18n.set_language', name="profile_set_language"),
    url(r'^reset/$', 'mpowering.profile.views.reset', name="profile_reset"),
    url(r'^reset/sent/$', TemplateView.as_view(template_name="mpowering/profile/reset-sent.html"), name="profile_reset_sent"),
    url(r'^edit/$', 'mpowering.profile.views.edit', name="profile_edit"),
)
