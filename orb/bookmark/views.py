# orb/bookmark/views.py

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseBadRequest, HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from orb.models import Resource, Collection, CollectionUser, CollectionResource


@login_required
@csrf_exempt
@require_POST
def resource_bookmark_view(request):
    """
    Creates a user bookmark for a resource

    Args:
        request: HTTP request

    Returns:
        a JSON HTTP response

    """

    resource_id = request.POST.get('resource_id')

    if resource_id is None:
        return HttpResponseBadRequest()

    resource = get_object_or_404(Resource, pk=resource_id)

    try:
        collection = Collection.objects.get(visibility=Collection.PRIVATE, collectionuser__user=request.user)
    except Collection.DoesNotExist:
        collection = Collection.objects.create(title="My Bookmarks")
        CollectionUser.objects.create(collection=collection, user=request.user)

    CollectionResource.objects.get_or_create(resource=resource, collection=collection)

    return JsonResponse({'success': True})


def resource_bookmark_remove_view(request, resource_id):
    if request.user.is_anonymous():
        raise Http404()
    # check the current user is the owner of this bookmark
    try:
        bookmark = CollectionResource.objects.get(
            resource__pk=resource_id, collection__visibility=Collection.PRIVATE, collection__collectionuser__user=request.user)
    except CollectionResource.DoesNotExist:
        return HttpResponseBadRequest()

    bookmark.delete()

    return HttpResponseRedirect(reverse('my_bookmarks_view'))
