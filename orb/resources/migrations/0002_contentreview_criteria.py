# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orb', '0027_auto_20160722_2028'),
        ('resources', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='contentreview',
            name='criteria',
            field=models.ManyToManyField(to='orb.ResourceCriteria', blank=True),
            preserve_default=True,
        ),
    ]
