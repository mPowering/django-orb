# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def update_status(apps, schema_editor):
    """Replace old 'active' status with published"""
    Course = apps.get_model('courses', 'Course')
    Course.objects.filter(status__icontains='active').update(status=b'published')


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(update_status),
    ]
