# orb/rating/views.py
import json

from django.conf import settings
from django.http import Http404, HttpResponse, HttpResponseBadRequest
from django.views.decorators.http import require_POST

from orb.models import Resource, ResourceRating


@require_POST
def resource_rate_view(request):
    if request.user.is_anonymous():
        raise Http404()

    resource_id = request.POST.get('resource_id')
    rating = request.POST.get('rating')

    if resource_id is None or rating is None:
        return HttpResponseBadRequest()

    rating = int(rating)
    if rating > 5 or rating < 1:
        return HttpResponseBadRequest()

    try:
        resource = Resource.objects.get(pk=resource_id)
    except Resource.DoesNotExist:
        return HttpResponseBadRequest()

    user_rating, created = ResourceRating.objects.get_or_create(
        resource=resource,
        user=request.user,
        defaults={'rating': rating},
    )
    if not created:
        user_rating.rating = rating
        user_rating.save()

    resp_obj = {
        'no_ratings': ResourceRating.objects.filter(resource=resource).count(),
        'ratings_required': settings.ORB_RESOURCE_MIN_RATINGS,
    }
    return HttpResponse(json.dumps(resp_obj), content_type="application/json; charset=utf-8")
