# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orb', '0035_auto_20161019_1415'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resourcecriteria',
            name='category',
            field=models.CharField(blank=True, max_length=50, null=True, help_text='deprecated', choices=[(b'qa', 'Quality Assurance'), (b'value', 'Value for Frontline Health Workers (FLHW)'), (b'video', 'Video resources'), (b'animation', 'Animation resources'), (b'audio', 'Audio resources'), (b'text', 'Text based resources')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='resourcecriteria',
            name='category_order_by',
            field=models.IntegerField(default=0, help_text='deprecated'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='resourceworkflowtracker',
            name='resource',
            field=models.ForeignKey(related_name='workflow_trackers', blank=True, to='orb.Resource', null=True),
            preserve_default=True,
        ),
    ]
