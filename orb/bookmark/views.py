# orb/bookmark/views.py
import json

from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse, HttpResponseBadRequest, HttpResponseRedirect

from orb.models import Resource, Collection, CollectionUser, CollectionResource


def resource_bookmark_view(request):
    if request.user.is_anonymous():
        raise Http404()
    if request.method == 'POST':
        resource_id = request.POST.get('resource_id')

        if resource_id is None:
            return HttpResponseBadRequest()

        resource = Resource.objects.get(pk=resource_id)
        # check if user already has a bookmark collection object
        try:
            collection = Collection.objects.get(
                visibility=Collection.PRIVATE, collectionuser__user=request.user)
        # if not create it
        except Collection.DoesNotExist:
            collection = Collection()
            collection.title = "My Bookmarks"
            collection.user = request.user
            collection.save()

            c_user = CollectionUser()
            c_user.collection = collection
            c_user.user = request.user
            c_user.save()

        # check if resource already bookmarked or not
        bookmarked = CollectionResource.objects.filter(
            resource=resource, collection=collection).count()
        if bookmarked == 0:
            cu = CollectionResource()
            cu.collection = collection
            cu.resource = resource
            cu.save()

        resp_obj = {}
        resp_obj['success'] = True

        return HttpResponse(json.dumps(resp_obj), content_type="application/json; charset=utf-8")
    else:
        return HttpResponseBadRequest()


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
