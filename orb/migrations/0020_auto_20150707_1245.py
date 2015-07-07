# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orb', '0019_resource_attribution'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='crt_member',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='mep_member',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
