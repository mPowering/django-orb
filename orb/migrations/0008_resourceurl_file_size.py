# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orb', '0007_auto_20150428_1804'),
    ]

    operations = [
        migrations.AddField(
            model_name='resourceurl',
            name='file_size',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
