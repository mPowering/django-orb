# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('orb', '0013_auto_20150506_1914'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resourcetracker',
            name='resource',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, default=None, blank=True, to='orb.Resource', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='resourcetracker',
            name='resource_file',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, default=None, blank=True, to='orb.ResourceFile', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='resourcetracker',
            name='resource_url',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, default=None, blank=True, to='orb.ResourceURL', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='resourcetracker',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, default=None, blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='resourceworkflowtracker',
            name='resource',
            field=models.ForeignKey(blank=True, to='orb.Resource', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='searchtracker',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, default=None, blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='tagtracker',
            name='tag',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, default=None, blank=True, to='orb.Tag', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='tagtracker',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, default=None, blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
    ]
