from django import forms
from django.utils.translation import ugettext_lazy as _

from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import FieldWithButtons, InlineCheckboxes
from crispy_forms.layout import Button, Layout, Fieldset, ButtonHolder, Submit, Div, HTML, Row

from mpowering.models import Tag, Resource, Organisation, Category

from tinymce.models import HTMLField

class ResourceCreateForm(forms.Form):
    title = forms.CharField(
                required=True,
                error_messages={'required': _('Please enter a title')},)
    organisations = forms.CharField(
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
                error_messages={},
                help_text=_('Either a file or a url is required'), )
    url = forms.CharField(
                required=False,
                error_messages={},)
    health_topic = forms.MultipleChoiceField(
                        widget=forms.CheckboxSelectMultiple,
                        required=True,
                        error_messages={'required': _('Please select at least one health topic')},)
    resource_type = forms.MultipleChoiceField(
                        widget=forms.CheckboxSelectMultiple,
                        required=True,
                        error_messages={'required': _('Please select at least one resource type')},)
    audience = forms.MultipleChoiceField(
                        widget=forms.CheckboxSelectMultiple,
                        required=True,
                        error_messages={'required': _('Please select at least one audience')},)
    geography = forms.MultipleChoiceField(
                        widget=forms.CheckboxSelectMultiple,
                        required=True,
                        error_messages={'required': _('Please select at least one geographical area')},)
    device = forms.MultipleChoiceField(
                        widget=forms.CheckboxSelectMultiple,
                        required=True,
                        error_messages={'required': _('Please select at least one device')},)
    license = forms.ChoiceField(
                        widget=forms.RadioSelect,
                        required=True,
                        error_messages={'required': _('Please select at least one license')},)
    other_tags = forms.CharField(
                        help_text=_('Please enter any other relevant tags for this resource, comma separated if entering more than one tag'),               
                        required=False,
                        )

    
    def __init__(self, *args, **kwargs):
        super(ResourceCreateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.layout = Layout(
                'title',
                'organisations',
                'description',
                'image',
                Row (HTML('<hr>')),
                'file',
                'url',
                Row (HTML('<hr>')),
                'health_topic',
                Row (HTML('<hr>')),
                'resource_type',
                Row (HTML('<hr>')),
                'audience',
                Row (HTML('<hr>')),
                'geography',
                Row (HTML('<hr>')),
                'device',
                Row (HTML('<hr>')),
                'license',
                Row (HTML('<hr>')),
                'other_tags',
                Row (HTML('<hr>')),
                Div(
                   Submit('submit', _(u'Save'), css_class='btn btn-default'),
                   css_class='col-lg-offset-2 col-lg-8',
                ),
            )
        
    def clean(self):
        cleaned_data = self.cleaned_data
        file = cleaned_data.get("file")
        url = cleaned_data.get("url").strip()
        if self._errors:
            raise forms.ValidationError( _(u"Please correct the errors below and resubmit the form."))
        if file is None and (url is None or url == ''):
            raise forms.ValidationError( _(u"Please submit a file and/or a url for this resource"))
        
        return self.cleaned_data
    
    def clean_file(self):
        file = self.cleaned_data['file']
        try:
            if file:
                file_type = file.content_type.split('/')[0]
                print file_type

                if len(file.name.split('.')) == 1:
                    raise forms.ValidationError(_('File type is not supported'))

                if file_type in settings.TASK_UPLOAD_FILE_TYPES:
                    if file._size > settings.TASK_UPLOAD_FILE_MAX_SIZE:
                        raise forms.ValidationError(_('Please keep filesize under %s. Current filesize %s') % (filesizeformat(settings.TASK_UPLOAD_FILE_MAX_SIZE), filesizeformat(file._size)))
                else:
                    raise forms.ValidationError(_('File type is not supported'))
        except:
            pass

        return file