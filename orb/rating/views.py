# orb/rating/views.py

from django.http import Http404, HttpResponse

from orb.models import Resource, ResourceRating



def resource_rate_view(request):
    if request.user.is_anonymous():
        raise Http404()
    if request.method == 'POST':
        resource_id = request.POST.get('resource_id')
        rating = request.POST.get('rating')
        #comment = request.POST.get('comment')
        
        try:
            resource = Resource.objects.get(pk=resource_id)
        except Resource.DoesNotExist:
            raise Http404()
        
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
        return HttpResponse()
    else:
        raise Http404()   
    