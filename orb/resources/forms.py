"""
Forms specific to working directly with resources
"""

from django import forms


class ResourceAccessForm(forms.Form):
    """
    Form class for collecting information prior to allowing a user to
    download a resource file or access a resource link.
    """
    survey_intended_use = forms.CharField(required=True)
    survey_intended_use_other = forms.CharField(required=False)
    survey_health_worker_count = forms.IntegerField(required=False)
    survey_health_worker_cadre = forms.CharField(required=False)
