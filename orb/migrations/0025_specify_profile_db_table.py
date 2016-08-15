# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orb', '0024_consolidate_resource_constants'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='userprofile',
            table='orb_userprofile',
        ),
    ]
