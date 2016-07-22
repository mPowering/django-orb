from django import forms

from orb.models import ResourceRating


class RatingForm(forms.ModelForm):

    class Meta:
        fields = '__all__'
        model = ResourceRating

    def save(self):
        """Prevent duplicates (per user/resource) and save"""
        try:
            self.instance = ResourceRating.objects.get(
                user=self.cleaned_data['user'],
                resource=self.cleaned_data['resource'],
            )
        except ResourceRating.DoesNotExist:
            pass

        super(RatingForm, self).save()