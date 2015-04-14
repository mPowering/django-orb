# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mpowering', '0002_auto_20150412_1735'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='gender',
            field=models.CharField(default=b'none', max_length=50, choices=[(b'female', 'Female'), (b'male', 'Male'), (b'none', 'Prefer not to say')]),
            preserve_default=True,
        ),
    ]
