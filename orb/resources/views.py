from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404

from orb.decorators import reviewer_required
from orb.models import Resource
from orb.resources.models import ContentReview


@reviewer_required
def review_resource(request, resource_id, review_id):
    """
    Renders/processes the form for adding a resource review.

    This view is restricted to the user assigned to the specific review.

    Args:
        request: HttpRequest
        resource_id: pk of the Resource
        review_id: pk of the ContentReview

    Returns:
        HttpResponse

    """
    review = get_object_or_404(ContentReview, pk=review_id, resource__pk=resource_id)
    if request.user != review.reviewer:
        raise PermissionDenied

    return render(request, "orb/resource/review_form.html", {})


@reviewer_required
def resource_review_list(request):
    """
    View that lists resources that are pending review
    """
    pending_resources = Resource.resources.pending()
    review_assignments = ContentReview.reviews.pending().for_user(request.user)

    return render(request, "orb/resource/review_list.html",{
        'pending_resources': pending_resources,
        'review_assignments': review_assignments,
    })
