# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orb', '0008_resourceurl_file_size'),
    ]

    operations = [
        migrations.AddField(
            model_name='resourcefile',
            name='image',
            field=models.ImageField(max_length=200, null=True, upload_to=b'resourceimage/%Y/%m/%d', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='resourceurl',
            name='image',
            field=models.ImageField(max_length=200, null=True, upload_to=b'resourceimage/%Y/%m/%d', blank=True),
            preserve_default=True,
        ),
    ]
