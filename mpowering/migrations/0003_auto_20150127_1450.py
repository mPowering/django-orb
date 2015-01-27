# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mpowering', '0002_tracker'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tracker',
            name='type',
            field=models.CharField(max_length=50, choices=[(b'view', 'View'), (b'edit', 'Edit'), (b'download', 'Download'), (b'create', 'Create'), (b'search', 'Search')]),
            preserve_default=True,
        ),
    ]
