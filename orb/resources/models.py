"""

"""

from django.conf import settings
from django.db import models
from django_fsm import FSMField, transition
from model_utils.models import TimeStampedModel

from orb.models import Resource


class ContentReview(TimeStampedModel):
    """
    Model class used to assign a content review for a resource to
    a content reviewer and to capture the review result.
    """
    # TODO this should be from the database to allow for multiple roles
    MEDICAL = 'medical'
    TECHNICAL = 'technical'
    OTHER = 'other'

    ROLES = [
        (MEDICAL, u'Medical'),
        (TECHNICAL, u'Technical'),
        (OTHER, u'Other'),
    ]

    resource = models.ForeignKey('orb.Resource', related_name="content_reviews")
    status = FSMField(default=Resource.PENDING)
    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL)
    notes = models.TextField(blank=True)
    role = models.CharField(max_length=10, choices=ROLES)

    @transition(field=status, source=Resource.PENDING, target=Resource.APPROVED)
    def approve(self):
        return None

    @transition(field=status, source=Resource.PENDING, target=Resource.REJECTED)
    def reject(self):
        return None


class ReviewLogEntry(TimeStampedModel):
    """
    Model class used to track individual actions made with regard
    to a resource's content review.

    """
    review = models.ForeignKey(ContentReview, related_name="log_entries")
    review_status = models.CharField(editable=False, max_length=20)


