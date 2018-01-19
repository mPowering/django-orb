# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orb', '0047_update_pending_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='survey',
            field=models.BooleanField(default=False),
        ),
    ]
