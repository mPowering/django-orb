
import json
import logging

from django import forms

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

    class Meta:
        model = models.Course
        fields = ['title', 'sections']

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
            json.dumps(data)
        except ValueError as e:
            logger.debug(e)
            raise forms.ValidationError("Invalid JSON")
        return data
