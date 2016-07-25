from datetime import datetime, timedelta

from django.utils.translation import ugettext as _

from orb.emailer import send_orb_email
from orb.resources.models import ContentReview


def send_review_reminder_email(review):
    """

    Args:
        review: a ContentReview

    Returns:
        None

    """
    send_orb_email(
        template_html="orb/email/review_reminder.html",
        template_text="orb/email/review_reminder.txt",
        subject=_(u"Pending review reminder"),
        recipients=review.reviewer.email,
        review=review,
        review_age_days=7,
    )


def remind_reviewers(start_days=7, end_days=8):
    """

    Args:
        start_days:
        end_days:

    Returns:

    """

    assert start_days < end_days

    pending_reviews = ContentReview.reviews.select_related().pending().filter(
        create_date__lte=datetime.utcnow() - timedelta(days=start_days),
        create_date__gt=datetime.utcnow() - timedelta(days=end_days),
    )

    for review in pending_reviews:
        send_review_reminder_email(review)
