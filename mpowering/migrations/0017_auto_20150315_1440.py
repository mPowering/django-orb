# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mpowering', '0016_resourcefile_file_full_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='api_access',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='resource',
            name='status',
            field=models.CharField(default=b'pending_crt', max_length=50, choices=[(b'rejected', 'Rejected'), (b'pending_crt', 'Pending CRT'), (b'pending_mrt', 'Pending MRT'), (b'approved', 'Approved')]),
            preserve_default=True,
        ),
    ]
