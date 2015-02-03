# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mpowering', '0006_resourcerating'),
    ]

    operations = [
        migrations.AddField(
            model_name='searchtracker',
            name='type',
            field=models.CharField(default=b'search', max_length=50, choices=[(b'search', 'search'), (b'search-api', 'search-api')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='resourcetracker',
            name='type',
            field=models.CharField(default=b'view', max_length=50, choices=[(b'view', 'View'), (b'view-api', 'View-api'), (b'edit', 'Edit'), (b'download', 'Download'), (b'create', 'Create')]),
            preserve_default=True,
        ),
    ]
