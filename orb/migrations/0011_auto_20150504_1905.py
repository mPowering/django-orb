# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orb', '0010_tagtracker'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tagtracker',
            name='type',
            field=models.CharField(default=b'view', max_length=50, choices=[(b'view', 'View'), (b'view-api', 'View-API'), (b'view-url', 'View-URL')]),
            preserve_default=True,
        ),
    ]
