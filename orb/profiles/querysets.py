from django.db import models


class ProfilesQueryset(models.QuerySet):
    """
    QuerySet class for UserProfiles
    """
    def reviewers(self):
        return self.filter(reviewer_roles__isnull=False)

    def nonreviewers(self):
        return self.filter(reviewer_roles__isnull=True)
