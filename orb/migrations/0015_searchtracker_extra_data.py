# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orb', '0014_auto_20150508_1718'),
    ]

    operations = [
        migrations.AddField(
            model_name='searchtracker',
            name='extra_data',
            field=models.TextField(default=None, null=True, blank=True),
            preserve_default=True,
        ),
    ]
