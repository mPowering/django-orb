# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orb', '0022_auto_20150825_1318'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resourcetracker',
            name='ip',
            field=models.GenericIPAddressField(default=None, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='searchtracker',
            name='ip',
            field=models.GenericIPAddressField(default=None, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='tagtracker',
            name='ip',
            field=models.GenericIPAddressField(default=None, null=True, blank=True),
            preserve_default=True,
        ),
    ]
