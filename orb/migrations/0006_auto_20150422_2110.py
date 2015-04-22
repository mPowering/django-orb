# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orb', '0005_resourcecriteria'),
    ]

    operations = [
        migrations.AddField(
            model_name='resourcecriteria',
            name='category',
            field=models.CharField(default=None, max_length=50, choices=[(b'qa', 'Quality Assurance'), (b'value', 'Value for Frontline Health Workers (FLHW)'), (b'video', 'Video resources'), (b'animation', 'Animation resources'), (b'audio', 'Audio resources'), (b'text', 'Text based resources')]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='resourcecriteria',
            name='category_order_by',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
