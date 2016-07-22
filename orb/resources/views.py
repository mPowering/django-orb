from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from django.utils.translation import ugettext_lazy as _

from orb.decorators import reviewer_required
from orb.models import Resource
from .forms import ReviewForm, RejectionForm
from .models import ContentReview


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
    review = get_object_or_404(
        ContentReview.objects.select_related(),
        pk=review_id,
        resource__pk=resource_id,
    )

    if request.user != review.reviewer:
        raise PermissionDenied

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            approved = form.cleaned_data['approved']
            if approved:
                review.approve()
                review.save()
                messages.success(request, _("Thank you for reviewing this content"))
            else:
                review.reject()
                review.save()
                messages.success(request, _("Thank you for reviewing this content"))
            return redirect("orb_pending_resources")
    else:
        form = ReviewForm()

    return render(request, "orb/resource/review_form.html", {
        'review': review,
        'form': form,
    })


@reviewer_required
def reject_resource(request, resource_id, review_id):
    review = get_object_or_404(
        ContentReview.objects.select_related(),
        pk=review_id,
        resource__pk=resource_id,
    )

    if request.user != review.reviewer:
        raise PermissionDenied

    if not review.is_pending:
        messages.info(request, _("You cannot review this content again."))
        return redirect("orb_pending_resources")

    form = RejectionForm()
    return render(request, "orb/resource/reject_form.html", {
        'form': form,
        'resource': review.resource,
    })



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
