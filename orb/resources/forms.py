"""
Forms specific to working directly with resources
"""
from __future__ import unicode_literals

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div, Layout, Submit
from django import forms
from django.utils.translation import ugettext_lazy as _

from orb.models import Tag


class ResourceAccessForm(forms.Form):
    """
    Form class for collecting information prior to allowing a user to
    download a resource file or access a resource link.
    """
    INTENDED_USE = [
        ("learning", _("For my own learning")),
        ("browsing", _("I'm just browsing")),
        ("training", _("For training frontline health workers")),
        ("other", _("Other")),
    ]

    survey_intended_use = forms.ChoiceField(
        label=_("Please let us know how you are intending to use this resource"),
        required=True,
        choices=INTENDED_USE,
        widget=forms.RadioSelect(),
    )
    survey_intended_use_other = forms.CharField(
        label=_("Please explain"),
        required=False,
        widget=forms.Textarea(),
    )
    survey_health_worker_count = forms.IntegerField(
        label=_("How many frontline health workers are you intending to train?"),
        required=False,
        min_value=1,
    )
    survey_health_worker_cadre = forms.ModelChoiceField(
        label=_("What type/cadre of frontline health workers are you intending to train?"),
        required=False,
        queryset=Tag.tags.approved().roles(),
    )

    def __init__(self, *args, **kwargs):
        super(ResourceAccessForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'GET'
        self.helper.form_class = 'form-horizontal'
        self.helper.disable_csrf = True
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.layout = Layout(
            'survey_intended_use',
            'survey_intended_use_other',
            'survey_health_worker_count',
            'survey_health_worker_cadre',
            Div(
                Submit('submit', _(u'Continue &gt;&gt;'),
                       css_class='btn btn-default'),
                css_class='col-lg-offset-2 col-lg-8',
            ),
        )
