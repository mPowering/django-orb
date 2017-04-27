# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orb', '0045_auto_20170414_1715'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='crt_member',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='mep_member',
        ),
    ]
