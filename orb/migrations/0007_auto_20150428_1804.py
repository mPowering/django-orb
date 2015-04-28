# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orb', '0006_auto_20150422_2110'),
    ]

    operations = [
        migrations.AddField(
            model_name='resourcefile',
            name='order_by',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='resourceurl',
            name='order_by',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
