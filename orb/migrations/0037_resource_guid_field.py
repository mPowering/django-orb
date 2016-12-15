# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orb', '0036_auto_20161123_0946'),
    ]

    operations = [
        migrations.AddField(
            model_name='resource',
            name='guid',
            field=models.UUIDField(unique=True, null=True, editable=False),
        ),
        migrations.AddField(
            model_name='resourcefile',
            name='guid',
            field=models.UUIDField(unique=True, null=True, editable=False),
        ),
        migrations.AddField(
            model_name='resourceurl',
            name='guid',
            field=models.UUIDField(unique=True, null=True, editable=False),
        ),
    ]
