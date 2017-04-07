
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

    page = forms.IntegerField(min_value=1, widget=forms.HiddenInput, initial=1)
    order = forms.ChoiceField(choices=ORDER_OPTIONS)
