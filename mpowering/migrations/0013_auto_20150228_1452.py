# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mpowering', '0012_auto_20150226_1106'),
    ]

    operations = [
        migrations.AddField(
            model_name='resourcefile',
            name='summary',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='resourceurl',
            name='summary',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
