"""
Forms for resources - primarily for content review
"""

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div, Layout, Submit
from django import forms
from django.utils.translation import ugettext as _

from orb.models import ResourceCriteria


class ReviewForm(forms.Form):
    """
    Form for allowing a reviewer to enter a resource review
    """
    approved = forms.BooleanField(required=False)
    reason = forms.CharField(required=False, widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.layout = Layout(
            'reason',
        )

    def clean(self):
        data = self.cleaned_data
        if not data.get('approved') and not data.get('reason'):
            raise forms.ValidationError(_("Please provide a reason for rejecting this content."))
        return data


class RejectionForm(forms.Form):
    criteria = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        queryset=ResourceCriteria.objects.all().order_by('category_order_by', 'order_by'),
        required=False,
    )
    notes = forms.CharField(
        widget=forms.Textarea,
        required=True,
        error_messages={'required': _(
            'Please enter a reason as to why the resource has been rejected')},
        help_text=_(
            'The text you enter here will be included in the email to the submitter of the '
            'resource, so please bear this in mind when explaining your reasoning.'),
        label=_(u"Reason for rejection")
    )

    def __init__(self, *args, **kwargs):
        super(RejectionForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.layout = Layout(
            'criteria',
            'notes',
            Div(
                Submit('submit', _(u'Submit'),
                       css_class='btn btn-default'),
                css_class='col-lg-offset-2 col-lg-8',
            ),
        )