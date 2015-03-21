# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mpowering', '0020_tagowner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resource',
            name='study_time_number',
            field=models.IntegerField(default=0, null=True, blank=True),
            preserve_default=True,
        ),
    ]
