# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mpowering', '0007_auto_20150203_1949'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='descripition',
            field=models.TextField(default=None, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='tag',
            name='external_url',
            field=models.URLField(default=None, max_length=500, null=True, blank=True),
            preserve_default=True,
        ),
    ]
