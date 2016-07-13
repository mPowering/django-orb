# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('orb', '0025_specify_profile_db_table'),
    ]

    operations = [
        migrations.AddField(
            model_name='resourcetag',
            name='update_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 7, 13, 17, 8, 56, 202546, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='resourceworkflowtracker',
            name='update_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 7, 13, 17, 9, 6, 42961, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
    ]
