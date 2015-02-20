# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mpowering', '0008_auto_20150206_1158'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resource',
            name='status',
            field=models.CharField(max_length=50, choices=[(b'rejected', 'Rejected'), (b'pending_crt', 'Pending CRT'), (b'pending_mrt', 'Pending MRT'), (b'approved', 'Approved')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='tag',
            name='image',
            field=models.ImageField(null=True, upload_to=b'tag/%Y/%m/%d', blank=True),
            preserve_default=True,
        ),
    ]
