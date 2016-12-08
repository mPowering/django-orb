# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('peers', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='peer',
            name='api_key',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='peer',
            name='api_user',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
    ]
