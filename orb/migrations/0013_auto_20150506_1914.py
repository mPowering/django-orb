# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orb', '0012_auto_20150505_1740'),
    ]

    operations = [
        migrations.AlterField(
            model_name='searchtracker',
            name='type',
            field=models.CharField(default=b'search', max_length=50, choices=[(b'search', 'search'), (b'search-api', 'search-api'), (b'search-adv', 'search-adv')]),
            preserve_default=True,
        ),
    ]
