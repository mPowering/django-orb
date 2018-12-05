"""
Oppia backup-format export for courses

"""
from __future__ import unicode_literals

import zipfile
from StringIO import StringIO

from django.template.loader import render_to_string
from lxml import etree

from orb.courses.export import CourseExport
from orb.courses.export import format_page_as_markdown

import os
from django.conf import settings

class OppiaExport(CourseExport):
    """
    Builds structure for exporting to an Oppia compatible format

    It starts from a base zip file that contains the common folders
    and files in an Oppia export.

    For each resource (file): write it to resources/file-name.
    The metadata goes in module.xml

    We track order of sections and order of activities in sectiosn

    everythign has a digest.


    """
    default_filename = "orb-course.zip"
    course_folder = "ORB_Course"  # Must match what's in the base archive

    def __init__(self, *args, **kwargs):
        super(OppiaExport, self).__init__(*args, **kwargs)

        for section in self.sections:
            for activity in section["activities"]:
                if activity["type"] == "page":
                    activity["html"] = self.page_filename(activity)

    def validate_backup_filename(self):
        if not self.backup_filename.endswith(".zip"):
            raise ValueError("Oppia backup file names must end with the .zip extension")

    def format_page(self, activity):
        return render_to_string("orb/courses/oppia_page.html", {
            "content": format_page_as_markdown(activity)
        }).encode("utf8")

    def page_filename(self, activity):
        return "{}_{}_{}.html".format(
            activity["section"],
            activity["digest"][-5:],
            "en",
        )

    def page_filename_fullpath(self, activity):
        return "{}/{}".format(
            self.course_folder,
            self.page_filename(activity),
        )

    def write_pages(self, backup_file):
        for course_resource in self.pages():
            page_html = self.format_page(course_resource)
            backup_file.writestr(
                self.page_filename_fullpath(course_resource),
                page_html,
            )

    def write_resources(self, backup_file):
        for course_resource in self.resources():
            with open(course_resource['file_path'], 'rb') as rf:
                backup_file.writestr(
                    "{}/resources/{}".format(
                        self.course_folder,
                        course_resource["file_name"],
                    ),
                    rf.read()
                )

    def module_xml(self, context):
        """Validates and returns the module.xml file contents"""
        oppia_xml = render_to_string(os.path.join(settings.COURSE_TEMPLATE_PATH, "orb/courses/templates", "orb/courses/oppia_module.xml"), context).encode("utf8")
        schema_source = etree.parse(os.path.join(settings.COURSE_TEMPLATE_PATH, "orb/courses/oppia-schema.xsd"))
        oppia_schema = etree.XMLSchema(schema_source)
        oppia_xml_tree = etree.fromstring(oppia_xml)
        oppia_schema.assertValid(oppia_xml_tree)
        return oppia_xml

    def module_context(self):
        return dict(
            shortname=self.name,
            title=self.name,
            versionid=1,
            oppia_server="",
            sections=self.sections,
        )

    def export(self, backup_file=None):
        """Performs the full backup"""
        if not backup_file:
            backup_file = StringIO()

        with open(os.path.join(settings.COURSE_TEMPLATE_PATH, "orb/courses/ORB_Course.zip.template"), "rb") as base_export_file:
            backup_file.write(base_export_file.read())
            backup_file.seek(0)

            with zipfile.ZipFile(
                backup_file, "a", compression=zipfile.ZIP_DEFLATED
            ) as updated_backup_file:
                updated_backup_file.writestr(
                    "{}/module.xml".format(self.course_folder),
                    self.module_xml(self.module_context()),
                )
                self.write_pages(updated_backup_file)
                self.write_resources(updated_backup_file)

        backup_file.seek(0)
        return backup_file
