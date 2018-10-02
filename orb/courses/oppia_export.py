"""
Oppia backup-format export for courses

"""
from __future__ import unicode_literals

import zipfile
from StringIO import StringIO

from django.template.loader import render_to_string

from orb.courses.export import CourseExport
from orb.courses.export import format_page_as_markdown


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

    def write_pages(self, backup_file):
        for course_resource in self.pages():
            page_html = self.format_page(course_resource)
            backup_file.writestr(
                self.page_filename(course_resource),
                page_html,
            )

    def write_resources(self, backup_file):
        for course_resource in self.resources():
            with open(course_resource['file_path'], 'rb') as rf:
                backup_file.writestr(
                    "resources/{}".format(course_resource["file_name"]),
                    rf.read()
                )

    def module_xml(self, context):
        """Returns the module.xml file contents"""
        return render_to_string("orb/courses/oppia_module.xml", context).encode("utf8")

    def module_context(self):
        return dict(
            shortname=self.name,
            title=self.name,
            versionid=1,
            oppia_server="",
            sections=self.sections,
        )

    def export(self):
        """Performs the full backup"""
        backup_file = StringIO()

        with open("orb/courses/oppia-export-base.zip", "rb") as base_export_file:
            backup_file.write(base_export_file.read())
            backup_file.seek(0)

            with zipfile.ZipFile(
                backup_file, "a", compression=zipfile.ZIP_DEFLATED
            ) as updated_backup_file:
                updated_backup_file.writestr(
                    "module.xml", self.module_xml(self.module_context())
                )
                self.write_pages(updated_backup_file)
                self.write_resources(updated_backup_file)

        backup_file.seek(0)
        return backup_file
