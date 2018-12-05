
from __future__ import unicode_literals

import json
import logging

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div, Layout, Submit
from django import forms
from django.utils.translation import ugettext_lazy as _

from orb.courses import models

logger = logging.getLogger(__name__)


class CourseAdminForm(forms.ModelForm):

    class Meta:
        model = models.Course
        fields = "__all__"

    def clean_sections(self):
        data = self.cleaned_data.get("sections", "[]")
        try:
            json.loads(data)
        except ValueError:
            raise forms.ValidationError("Invalid JSON. Try checking this using https://jsonlint.com/")
        return data


class CourseForm(forms.ModelForm):

    status = forms.ChoiceField(
        choices=models.CourseStatus.as_choices(),
        required=False,
        initial=models.CourseStatus.initial(),
    )

    class Meta:
        model = models.Course
        fields = ['title', 'sections', 'status']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(CourseForm, self).__init__(*args, **kwargs)

    def save(self, **kwargs):
        if not getattr(self.instance, 'pk', None):
            self.instance.create_user = self.user
        self.instance.update_user = self.user
        return super(CourseForm, self).save(**kwargs)

    def clean_sections(self):
        data = self.cleaned_data.get("sections", "[]")
        try:
            json.loads(data)
        except ValueError as e:
            logger.debug(e)
            raise forms.ValidationError("Invalid JSON")
        return data


class OppiaPublishForm(forms.Form):
    """"""
    host = forms.URLField()
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    tags = forms.CharField()
    is_draft = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        super(OppiaPublishForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal'
        # self.helper.disable_csrf = True
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.layout = Layout(
            'host',
            'username',
            'password',
            'tags',
            'is_draft',
            Div(
                Submit('submit', _("Publish"),
                       css_class='btn btn-default'),
                css_class='col-lg-offset-2 col-lg-8',
            ),
        )

    def clean_tags(self):
        tags = self.cleaned_data.get("tags", "").strip().split(",")
        cleaned_tags = [tag.strip() for tag in tags if tag.strip()]
        if not cleaned_tags:
            raise forms.ValidationError("At least one tag is required, use commas to separate multiple tags")
        return ",".join(cleaned_tags)
