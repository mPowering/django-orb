from datetime import datetime, timedelta

from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site
from django.utils.translation import ugettext as _

from orb.emailer import send_orb_email


def send_review_assignment_email(review):
    """
    Sends an email to the assigned reviewer for the given review.

    Args:
        review: a ContentReview

    Returns:
        result of `send_mail` - 1 or 0

    """
    return send_orb_email(
        template_html="orb/email/review_assignment.html",
        template_text="orb/email/review_assignment.txt",
        subject=_(u"New content review assignment"),
        recipients=[review.reviewer.email],
        review=review,
    )


def send_review_reminder_email(review):
    """

    Args:
        review: a ContentReview

    Returns:
        result of `send_mail` - 1 or 0

    """
    return send_orb_email(
        template_html="orb/email/review_reminder.html",
        template_text="orb/email/review_reminder.txt",
        subject=_(u"Pending review reminder"),
        recipients=[review.reviewer.email],
        review=review,
        review_age_days=7,
    )


def remind_reviewers(start_days=7, end_days=8):
    """

    Args:
        start_days:
        end_days:

    Returns:
        None

    """
    from orb.review.models import ContentReview

    assert start_days < end_days

    pending_reviews = ContentReview.reviews.select_related().pending().filter(
        create_date__lte=datetime.utcnow() - timedelta(days=start_days),
        create_date__gt=datetime.utcnow() - timedelta(days=end_days),
    )

    for review in pending_reviews:
        send_review_reminder_email(review)


def send_resource_approved_email(resource):
    current_site = Site.objects.get_current()
    return send_orb_email(
        template_html="orb/email/resource_approved.html",
        template_text="orb/email/resource_approved.txt",
        subject=_(u"Resource Submission") + ": " + resource.title,
        recipients=[resource.create_user.email],
        title=resource.title,
        firstname=resource.create_user.first_name,
        lastname=resource.create_user.last_name,
        info_email=settings.ORB_INFO_EMAIL,
        resource_link=current_site.domain + reverse('orb_resource', args=[resource.slug]),
    )


def send_resource_rejected_email(resource):
    current_site = Site.objects.get_current()
    return send_orb_email(
        template_html="orb/email/resource_rejected.html",
        template_text="orb/email/resource_rejected.txt",
        subject=_(u"Resource Submission") + ": " + resource.title,
        recipients=[resource.create_user.email],
        title=resource.title,
        firstname=resource.create_user.first_name,
        lastname=resource.create_user.last_name,
        info_email=settings.ORB_INFO_EMAIL,
        resource_link=current_site.domain + reverse('orb_resource', args=[resource.slug]),
    )


def send_review_complete_email(resource, **kwargs):
    """
    Sends an email to staff recipients that all reviews for the given
    resource have been completed.
    """
    current_site = Site.objects.get_current()
    return send_orb_email(
        template_html="orb/email/review_complete.html",
        template_text="orb/email/review_complete.txt",
        subject=_(u"Resource Review Complete") + ": " + resource.title,
        recipients=[settings.ORB_INFO_EMAIL],
        title=resource.title,
        firstname=resource.create_user.first_name,
        lastname=resource.create_user.last_name,
        resource_link=current_site.domain + reverse('orb_resource', args=[resource.slug]),
        **kwargs
    )
