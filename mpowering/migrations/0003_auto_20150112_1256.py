# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mpowering', '0002_auto_20150112_1208'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tag',
            options={'verbose_name': 'Tag', 'verbose_name_plural': 'Tags'},
        ),
        migrations.RenameField(
            model_name='category',
            old_name='ref',
            new_name='slug',
        ),
        migrations.AddField(
            model_name='resource',
            name='status',
            field=models.CharField(default=None, max_length=50, choices=[(b'rejected', 'Rejected'), (b'pending', 'Pending'), (b'approved', 'Approved')]),
            preserve_default=False,
        ),
    ]
