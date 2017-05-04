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
        migrations.AlterField(
            model_name='resource',
            name='status',
            field=models.CharField(default=b'pending', max_length=50, choices=[(b'approved', 'Approved'), (b'pending', 'Pending'), (b'rejected', 'Rejected'), (b'archived', 'Archived')]),
        ),
        migrations.AlterField(
            model_name='resourceworkflowtracker',
            name='status',
            field=models.CharField(default=b'pending', max_length=50, choices=[(b'approved', 'Approved'), (b'pending', 'Pending'), (b'rejected', 'Rejected'), (b'archived', 'Archived')]),
        ),
    ]
