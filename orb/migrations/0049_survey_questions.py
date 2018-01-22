# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orb', '0048_userprofile_survey'),
    ]

    operations = [
        migrations.AddField(
            model_name='resourcetracker',
            name='survey_health_worker_cadre',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='resourcetracker',
            name='survey_health_worker_count',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='resourcetracker',
            name='survey_intended_use',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='resourcetracker',
            name='survey_intended_use_other',
            field=models.TextField(default=b'', null=True, blank=True),
        ),
    ]
