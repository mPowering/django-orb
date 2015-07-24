# orb/rating/views.py
import json

from django.conf import settings
from django.http import Http404, HttpResponse, HttpResponseBadRequest

from orb.models import Resource, ResourceRating



def resource_rate_view(request):
    if request.user.is_anonymous():
        raise Http404()
    if request.method == 'POST':
        resource_id = request.POST.get('resource_id')
        rating = request.POST.get('rating')
        #comment = request.POST.get('comment')
        
        if resource_id is None or rating is None:
            return HttpResponseBadRequest()
        
        rating = int(rating)
        if rating > 5 or rating < 1: 
            return HttpResponseBadRequest()
        
        try:
            resource = Resource.objects.get(pk=resource_id, status=Resource.APPROVED)
        except Resource.DoesNotExist:
            return HttpResponseBadRequest()
        
        # check if an update or new rating
        try:
            user_rated = ResourceRating.objects.get(resource=resource,user=request.user)
            user_rated.rating = rating
            user_rated.save()
        except ResourceRating.DoesNotExist:
            rating_obj = ResourceRating() 
            rating_obj.resource = resource
            rating_obj.rating = rating
            rating_obj.user = request.user
            rating_obj.save()
        
        resp_obj = {}    
        resp_obj['no_ratings'] = ResourceRating.objects.filter(resource=resource).count()
        resp_obj['ratings_required'] = settings.ORB_RESOURCE_MIN_RATINGS
        return HttpResponse(json.dumps(resp_obj),content_type="application/json; charset=utf-8")
    else:
        return HttpResponseBadRequest()   
    