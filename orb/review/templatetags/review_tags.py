"""
Template labels for content review
"""

from django import template

from orb.models import ReviewerRole

register = template.Library()


@register.inclusion_tag("orb/review/_status_labels.html")
def status_labels(resource):
    """
    Renders tag labels for the individual reviews (assigned or
    unassigned by role) for a given resource.

    Args:
        resource: an orb.Resource under review

    Returns:
        Rendered template

    """
    roles = list(ReviewerRole.objects.all())

    reviews = resource.content_reviews.all()
    assigned_reviews= {review.role: review for review in reviews}

    assignments = {}
    for role in roles:
        assigned = assigned_reviews.get(role)
        if not assigned:
            assignments[role.name] = {
                'status': 'unassigned',
                'class': 'default',
            }
        else:
            if assigned.is_overdue:
                assignments[role.name] = {
                    'status': 'overdue',
                    'class': 'warning',
                }
            elif assigned.is_pending:
                assignments[role.name] = {
                    'status': 'pending',
                    'class': 'info',
                }
            else:
                assignments[role.name] = {
                    'status': 'complete',
                    'class': 'success',
                }

    return {
        'assignments': assignments,
    }