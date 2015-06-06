# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orb', '0018_userprofile_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='resource',
            name='attribution',
            field=models.TextField(default=None, null=True, blank=True),
            preserve_default=True,
        ),
    ]
