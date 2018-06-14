# -*- coding: utf-8 -*-

"""
Models for ORB courses
"""

from __future__ import unicode_literals

import json
import logging

from autoslugged.settings import slugify
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext
from enum import Enum

from orb.courses.export import MoodleCourse
from orb.models import TimestampBase
from orb.models import ResourceFile


logger = logging.getLogger('orb.courses')


class BaseChoices(Enum):
    @classmethod
    def as_choices(cls):
        return [
            (child.name, child.name)
            for child in cls
        ]

    @classmethod
    def initial(cls):
        """By default returns the first item"""
        for child in cls:
            return child.name


class CourseStatus(BaseChoices):
    draft = ugettext("Draft")
    published = ugettext("Published")
    archived = ugettext("Archived")


class CourseQueryset(models.QuerySet):

    def active(self):
        return self.exclude(status=CourseStatus.archived.name)

    def published(self):
        return self.filter(status=CourseStatus.published.name)

    def archived(self):
        return self.filter(status=CourseStatus.archived.name)

    def viewable(self, user):
        """Returns only those itesm the given user should be able to see"""
        if user == AnonymousUser():
            return self.published()
        if user.is_staff:
            return self.active()
        return self.filter(
            models.Q(status=CourseStatus.published.name) |
            models.Q(status=CourseStatus.draft.name, create_user=user)
        )

    def editable(self, user):
        """Returns only those itesm the given user should be able to edit"""
        if user == AnonymousUser():
            return self.none()
        if user.is_staff:
            return self.active()
        return self.active().filter(create_user=user)


class Course(TimestampBase):
    """
    Data container for a user-created course
    """
    status = models.CharField(
        max_length=50,
        choices=CourseStatus.as_choices(),
        default=CourseStatus.draft.name,
    )
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

    def section_data(self):
        """Returns serialized section data"""
        return json.loads(self.sections)

    def moodle_sections(self):
        """Returns section only data"""
        sections = []
        resource_count = 1

        for index, section in enumerate(self.section_data(), start=1):
            start = resource_count
            end = resource_count + len(section) + 1
            sections.append({'id': index, 'sequence': [i for i in range(start, end)]})
            resource_count += len(section)

        return sections

    def resource_files(self):
        """
        Filters activities by resources (files)
        """
        for section in self.section_data():
            for resource in section["resources"]:
                if resource["type"] == "CourseResource":
                    file_data = {}
                    file_data.update(**resource)
                    try:
                        rf = ResourceFile.objects.get(pk=file_data["id"])
                    except ResourceFile.DoesNotExist:
                        logger.error("ResourceFile missing for export, pk: '{}'".format(file_data["id"]))
                        continue

                    file_data.update({
                        "file_path": rf.full_path,
                        "file_sha1": rf.sha1sum(),
                        "file_size": rf.filesize(),
                    })

                    yield file_data


    def moodle_activities(self):
        # type: () -> (dict, dict)
        """
        Returns dictionaries of Moodle section and activities content

        Build dictionaries of sections and activities with unique identifiers

        The sections must map the sequence of activities, referencing the activities
        by ID, and the activities must reference their section by ID.

        For this data::

            >>> data = [{
                    "resources": [{
                        "type": "CourseActivity",
                        "description": "Hello world",
                        "title": "First slide"
                    }, {
                        "type": "CourseActivity",
                        "description": "Olé!",
                        "title": "Intermission"
                    }]
                }, {
                    "resources": [{
                        "type": "CourseActivity",
                        "description": "Second section description",
                        "title": "Second section title"
                    }]
                }]

        This should result in data looking like so::

            >>> course = Course(sections=data)
            >>> sections, activities = course.moodle_activities()
            >>> sections
            [{'id': 1, 'sequence': [1, 2]}, {'id': 2, 'sequence': [3]}]

        Returns:
            tuple of dictionaries describing the data

        """
        sections = []
        activities = []
        resource_id = 1

        def render_page_activity(activity, resource_id, section_count):
            if activity.get("type") == "CourseResource":
                rf = ResourceFile.objects.get(pk=activity["id"])
                sha1 = rf.sha1sum()
                return {
                    'id': resource_id,
                    'type': 'resource',
                    'intro': activity['title'],
                    'content': activity['description'],
                    'section': section_count,
                    "file_path": rf.full_path,
                    "file_sha": sha1,
                    "file_size": rf.filesize(),
                    "export_path": "files/{}/{}".format(sha1[:2], sha1),
                }
            return {
                'id': resource_id,
                'type': 'page',
                'intro': activity['title'],
                'content': activity['description'],
                'section': section_count,
            }

        for section_count, section in enumerate(self.section_data(), start=1):
            section_activities = []
            for activity in section['resources']:
                activities.append(render_page_activity(activity, resource_id, section_count))
                section_activities.append(resource_id)
                resource_id += 1
            sections.append({'id': section_count, 'sequence': section_activities})

        return sections, activities

    @property
    def moodle_file_name(self):
        """
        Returns the slugified title with an mbz extension
        """
        return "{}.mbz".format(slugify(self.title))

    def moodle_backup(self):
        """
        Returns an archive of the course in zipped Moodle backup format

        """
        sections, activities = self.moodle_activities()
        backup = MoodleCourse(
            name=self.title,
            id=self.pk,
            sections=sections,
            activities=activities,
            backup_filename=self.moodle_file_name,
        )
        return backup.export()
