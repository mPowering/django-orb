from django import forms
from django.utils.translation import ugettext_lazy as _

from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import FieldWithButtons, InlineCheckboxes
from crispy_forms.layout import Button, Layout, Fieldset, ButtonHolder, Submit, Div, HTML, Row

from mpowering.models import Tag, Resource, Organisation, Category

class ResourceCreateForm(forms.Form):
    title = forms.CharField(
                required=True,
                error_messages={'required': _('Please enter a title')},)
    organisation = forms.CharField(
                help_text=_('Comma separated if entering more than one organisation'),               
                required=True,
                error_messages={'required': _('Please enter at least one organisation')},)
    description = forms.CharField(
                widget=forms.Textarea,
                required=True,
                error_messages={'required': _('Please enter a description')},)
    image = forms.ImageField(
                required=False,
                error_messages={},)
    file = forms.FileField(
                required=False,
                error_messages={},)
    url = forms.CharField(
                required=False,
                error_messages={},)
    health_topic = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple)
    resource_type = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple)
    audience = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple)
    geography = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple)
    device = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple)
    license = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple)

    
    def __init__(self, *args, **kwargs):
        super(ResourceCreateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.layout = Layout(
                'title',
                'organisation',
                'description',
                'image',
                'file',
                'url',
                'health_topic',
                'resource_type',
                'audience',
                'geography',
                'device',
                'license',
                Div(
                   Submit('submit', _(u'Save'), css_class='btn btn-default'),
                   css_class='col-lg-offset-2 col-lg-8',
                ),
            )
        
class TagForm(forms.Form):
    name = forms.BooleanField()
    