from __future__ import unicode_literals
from django import forms
from django.utils.translation import ugettext as _


class TagPageForm(forms.Form):

    CREATED = u'-create_date'
    TITLE = u'title'
    UPDATED = u'-update_date'
    RATING = u'-rating'
    ORDER_OPTIONS = (
        (CREATED, _(u'Create date')),
        (TITLE, _(u'Title')),
        (RATING, _(u'Rating')),
        (UPDATED, _(u'Update date')),
    )

    page = forms.CharField(widget=forms.HiddenInput, initial='1')
    order = forms.ChoiceField(choices=ORDER_OPTIONS, required=False)

    def clean_order(self):
        order = self.cleaned_data.get('order', self.CREATED)
        return order or self.CREATED

    def clean_page(self):
        page = self.cleaned_data.get('page', 1)
        try:
            page_value = int(page)
        except (ValueError, TypeError):
            raise forms.ValidationError("'{}' is not a valid page number".format(page))
        if page_value > 0:
            return page_value
        raise forms.ValidationError("'{}' is not a valid page number".format(page_value))
