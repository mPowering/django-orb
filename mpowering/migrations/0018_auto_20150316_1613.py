# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mpowering', '0017_auto_20150315_1440'),
    ]

    operations = [
        migrations.AddField(
            model_name='resource',
            name='study_time_number',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='resource',
            name='study_time_unit',
            field=models.CharField(blank=True, max_length=10, null=True, choices=[(b'mins', 'Mins'), (b'hours', 'Hours'), (b'days', 'Days'), (b'weeks', 'Weeks')]),
            preserve_default=True,
        ),
    ]
