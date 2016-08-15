# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orb', '0023_auto_20151028_2050'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resourceworkflowtracker',
            name='status',
            field=models.CharField(default=b'pending_crt', max_length=50, choices=[(b'rejected', 'Rejected'), (b'pending_crt', 'Pending CRT'), (b'pending_mrt', 'Pending MRT'), (b'approved', 'Approved')]),
            preserve_default=True,
        ),
    ]
