from functools import wraps

from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from django.utils.translation import ugettext_lazy as _

from orb.decorators import reviewer_required
from orb.models import Resource
from .forms import ReviewForm, RejectionForm, AssignmentForm
from .models import ContentReview


def resource_review(func):
    """View decorator that gets the matching review"""
    @wraps(func)
    def decorator(request, resource_id, review_id):
        review = get_object_or_404(
            ContentReview.objects.select_related(),
            pk=review_id,
            resource__pk=resource_id,
        )
        if request.user != review.reviewer:
            raise PermissionDenied
        return func(request, review)
    return decorator


@reviewer_required
@resource_review
def review_resource(request, review):
    """
    Renders/processes the form for adding a resource review.

    Args:
        request: the HttpRequest
        review: the selected review instance

    Returns:
        HttpResponse

    """
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            approved = form.cleaned_data['approved']
            if approved:
                review.approve()
                review.save()
                messages.success(request, _(u"Thank you for reviewing this content"))
            else:
                review.reject()
                review.save()
                messages.success(request, _(u"Thank you for reviewing this content"))
            return redirect("orb_pending_resources")
    else:
        form = ReviewForm()

    return render(request, "orb/resource/review_form.html", {
        'review': review,
        'form': form,
    })


@reviewer_required
@resource_review
def reject_resource(request, review):
    """
    View that handles

    Args:
        request: the HttpRequest
        review: the selected review instance

    Returns:
        HttpResponse

    """
    if not review.is_pending:
        messages.info(request, _(u"You cannot review this content again."))
        return redirect("orb_pending_resources")

    if request.method == 'POST':
        form = RejectionForm(request.POST, instance=review)
        if form.is_valid():
            review = form.save(commit=False)
            review.reject()
            review.save()
            messages.success(request, _(u"Thank you for reviewing this content"))
            return redirect("orb_pending_resources")
    else:
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


@reviewer_required
def assign_review(request, resource_id):

    resource = get_object_or_404(Resource, pk=resource_id)
    if request.method == 'POST':
        form = AssignmentForm(resource=resource, data=request.POST)
        if form.is_valid():
            form.save()
        else:
            print("Errors", form.errors)

    else:
        form = AssignmentForm(resource=resource)

    return render(request, "orb/resource/assign_review.html",{
        'resource': resource,
        'form': form,
    })
