# -*- coding: utf-8 -*-

"""
Models for ORB courses
"""

from __future__ import unicode_literals

import json

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models

from orb.models import TimestampBase


class CourseQueryset(models.QuerySet):

    def active(self):
        return self.filter(status='active')

    def editable(self, user):
        return self.all() if user.is_staff else self.filter(create_user=user)


class Course(TimestampBase):
    """
    Data container for a user-created course
    """
    STATUS_CHOICES = [('active', 'active'), ('archived', 'archived')]
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='active')
    create_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='course_create_user')
    update_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='course_update_user')

    title = models.CharField(max_length=200)

    # Previous work with a third party JSON field was unsuccessufl
    sections = models.TextField(default="[]")  # TODO use a proper JSON field

    courses = CourseQueryset.as_manager()
    objects = courses

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("courses_edit", kwargs={"pk": self.pk})

    def sections_as_json(self):
        return json.dumps(json.loads(self.sections))
