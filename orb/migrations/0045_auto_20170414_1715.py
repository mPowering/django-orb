# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orb', '0044_auto_20170406_1927'),
    ]

    operations = [
        migrations.AddField(
            model_name='resource',
            name='tags',
            field=models.ManyToManyField(to='orb.Tag', through='orb.ResourceTag', blank=True),
        ),
        migrations.AlterField(
            model_name='resourcetag',
            name='tag',
            field=models.ForeignKey(related_name='resourcetag', to='orb.Tag'),
        ),
        migrations.AlterField(
            model_name='tagowner',
            name='tag',
            field=models.ForeignKey(related_name='owner', to='orb.Tag'),
        ),
        migrations.AlterField(
            model_name='tagproperty',
            name='tag',
            field=models.ForeignKey(related_name='properties', to='orb.Tag'),
        ),
        migrations.AlterField(
            model_name='tagtracker',
            name='tag',
            field=models.ForeignKey(related_name='tracker', on_delete=django.db.models.deletion.SET_NULL, default=None, blank=True, to='orb.Tag', null=True),
        ),
    ]
