import json

from django import forms
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST

from orb.models import Resource, ResourceRating


class RatingForm(forms.ModelForm):

    rating = forms.IntegerField(min_value=1, max_value=5)

    class Meta:
        fields = '__all__'
        model = ResourceRating


@login_required
@require_POST
def resource_rate_view(request):

    form = RatingForm(data=request.POST)

    if not form.is_valid():
        return HttpResponseBadRequest()

    form.save()
    resource = form.cleaned_data['resource']

    resp_obj = {
        'no_ratings': ResourceRating.objects.filter(resource=resource).count(),
        'ratings_required': settings.ORB_RESOURCE_MIN_RATINGS,
    }

    return HttpResponse(json.dumps(resp_obj), content_type="application/json; charset=utf-8")
