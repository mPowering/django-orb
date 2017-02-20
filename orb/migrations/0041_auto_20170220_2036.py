# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orb', '0040_add_tracking_fields'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resource',
            name='source_url',
            field=models.URLField(help_text='Original resource URL.', null=True, blank=True),
        ),
    ]
