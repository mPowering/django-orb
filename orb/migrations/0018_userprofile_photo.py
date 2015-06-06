# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orb', '0017_auto_20150605_1823'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='photo',
            field=models.ImageField(max_length=200, null=True, upload_to=b'userprofile/%Y/%m/%d', blank=True),
            preserve_default=True,
        ),
    ]
