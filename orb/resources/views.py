"""

"""

from __future__ import unicode_literals

import logging

from django.http import Http404
from django.shortcuts import redirect
from django.views.generic import DetailView
from django.views.generic.edit import FormMixin

from orb.models import ResourceFile
from orb.models import ResourceURL
from orb.resources.forms import ResourceAccessForm
from orb.signals import resource_file_viewed
from orb.signals import resource_url_viewed

logger = logging.getLogger(__name__)


class ResourceComponentView(FormMixin, DetailView):
    model = None
    signal = None
    signal_arg_name = None
    pk_url_kwarg = 'id'
    form_class = ResourceAccessForm

    def send_signal(self):
        kwargs = {
            'request': self.request,
            self.signal_arg_name: self.object,
        }
        self.signal.send(sender=self.object, **kwargs)

    def get_queryset(self):
        return self.model.objects.approved(self.request.user)

    def form_valid(self, form):
        self.send_signal()
        return redirect(self.get_success_url())

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        return self.form_valid(form)


class ResourceFileView(ResourceComponentView):
    model = ResourceFile
    signal = resource_file_viewed
    signal_arg_name = 'resource_file'

    def get_object(self, queryset=None):
        object = super(ResourceFileView, self).get_object(queryset)
        if not object.filesize():
            logger.warning("File for '{}' does not exist or has 0 filesize".format(self.object))
            raise Http404
        return object

    def get_success_url(self):
        return self.object.full_path


class ResourceURLView(ResourceComponentView):
    model = ResourceURL
    signal = resource_url_viewed
    signal_arg_name = 'resource_url'

    def get_success_url(self):
        return self.object.url

