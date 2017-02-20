# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('peers', '0002_api_credentials'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='peerquerylog',
            options={'get_latest_by': 'finished'},
        ),
        migrations.AddField(
            model_name='peerquerylog',
            name='filtered_date',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='peerquerylog',
            name='new_resources',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='peerquerylog',
            name='skipped_local_resources',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='peerquerylog',
            name='unchanged_resources',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='peerquerylog',
            name='updated_resources',
            field=models.PositiveIntegerField(null=True),
        ),
    ]
