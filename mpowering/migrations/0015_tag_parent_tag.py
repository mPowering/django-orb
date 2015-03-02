# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mpowering', '0014_auto_20150228_1454'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='parent_tag',
            field=models.ForeignKey(default=None, blank=True, to='mpowering.Tag', null=True),
            preserve_default=True,
        ),
    ]
