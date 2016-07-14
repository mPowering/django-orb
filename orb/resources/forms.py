"""
Forms for resources - primarily for content review
"""

from django import forms
from django.utils.translation import ugettext as _


class ReviewForm(forms.Form):
    """
    Form for allowing a reviewer to enter a resource review
    """
    approved = forms.BooleanField(required=False)
    reason = forms.CharField(required=False, widget=forms.Textarea)

    def clean(self):
        data = self.cleaned_data
        if not data.get('approved') and not data.get('reason'):
            raise forms.ValidationError(_("Please provide a reason for rejecting this content."))
        return data
