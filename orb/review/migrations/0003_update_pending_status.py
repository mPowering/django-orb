# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def update_status(apps, schema_editor):
    """Replace old pending_mep and pending_crt resources"""
    ContentReview = apps.get_model("review", "ContentReview")
    ContentReview.objects.filter(status__icontains="pending").update(status=b'pending')


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0002_auto_20161017_0013'),
    ]

    operations = [
        migrations.RunPython(update_status),
    ]
