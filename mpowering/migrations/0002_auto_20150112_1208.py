# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mpowering', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='order_by',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='category',
            name='ref',
            field=models.CharField(default=None, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tag',
            name='order_by',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
