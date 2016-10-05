# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orb', '0033_auto_20161004_2026'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resourcecriteria',
            name='category',
            field=models.CharField(blank=True, max_length=50, null=True, choices=[(b'qa', 'Quality Assurance'), (b'value', 'Value for Frontline Health Workers (FLHW)'), (b'video', 'Video resources'), (b'animation', 'Animation resources'), (b'audio', 'Audio resources'), (b'text', 'Text based resources')]),
            preserve_default=True,
        ),
    ]
