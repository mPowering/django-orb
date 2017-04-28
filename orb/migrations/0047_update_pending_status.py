# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def update_status(apps, schema_editor):
    """Replace old pending_mep and pending_crt resources"""
    Resource = apps.get_model("orb", "Resource")
    Resource.objects.filter(status__icontains="pending").update(status=b'pending')


class Migration(migrations.Migration):

    dependencies = [
        ('orb', '0046_remove_mep_crt'),
    ]

    operations = [
        migrations.RunPython(update_status),
    ]
