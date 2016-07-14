from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404

from orb.decorators import reviewer_required
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