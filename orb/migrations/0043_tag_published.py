# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orb', '0042_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='published',
            field=models.BooleanField(default=True, help_text=b'Used to toggle status of health domains.'),
        ),
    ]
