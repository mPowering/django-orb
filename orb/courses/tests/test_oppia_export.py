# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import os

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from xmldiff import main as differ

from orb.courses.models import Course
from orb.courses.oppia_export import OppiaExport
from orb.models import ResourceFile

pytestmark = pytest.mark.django_db


# TODO fixture for a course or course content
# consider adding a whole course wiht actual resources including a test file


@pytest.fixture
def orb_resource_file(test_resource):
    yield ResourceFile.objects.create(
        resource=test_resource, file=SimpleUploadedFile("1pixel.jpg", b"")
    )


@pytest.fixture
def orb_course(testing_user, test_resource):
    yield Course.objects.create(
        create_user=testing_user,
        update_user=testing_user,
        title="My Test",
        sections=[
            {
                "resources": [
                    {
                        "type": "CourseActivity",
                        "description": "Hello world\n\nNice to meet you.",
                        "title": "First slide",
                    },
                    {
                        "type": "CourseActivity",
                        "description": "Olé!",
                        "title": "Intermission",
                    },
                ]
            },
            {
                "resources": [
                    {
                        "type": "CourseActivity",
                        "description": "Second section description",
                        "title": "Second section title",
                    }
                ]
            },
        ],
    )


def test_backup_filename(orb_course):
    """Ensure the filename is reported as expected"""
    assert orb_course.oppia_file_name == "my-test.zip"


def test_backup_exporter(orb_course):
    """Ensure this """
    assert isinstance(orb_course.oppia_exporter(), OppiaExport)


def test_module_xml(orb_course):
    """Ensure the module.xml content is built as expected

    Test against an existing XML file by reading into memory
    """
    oppia_exporter = orb_course.oppia_exporter()  # type: OppiaExport
    expected_file_path = os.path.join(os.path.dirname(__file__), "expected_module.xml")

    with open(expected_file_path, "r") as expected_file:
        # expected_xml = ET.fromstring(expected_file.read())
        diff = differ.diff_texts(
            expected_file.read(),
            oppia_exporter.module_xml(oppia_exporter.module_context()),
        )
        assert not diff
        # assert expected_xml == result_xml


def test_publish_to_oppia(client, orb_course):
    """Test that the page loads"""
    response = client.get(reverse("courses_oppia_publish", kwargs={"pk": orb_course.pk}))
    assert response.status_code == 200
