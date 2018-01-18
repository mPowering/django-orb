# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orb', '0048_add_registration_flag'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='survey',
            field=models.BooleanField(default=False),
        ),
    ]
