# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import orb.fields


class Migration(migrations.Migration):

    dependencies = [
        ('orb', '0023_auto_20151028_2050'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=orb.fields.AutoSlugField(null=True, populate_from=b'name', editable=False, max_length=100, blank=True, unique=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='collection',
            name='slug',
            field=orb.fields.AutoSlugField(null=True, populate_from=b'title', editable=False, max_length=255, blank=True, unique=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='resource',
            name='slug',
            field=orb.fields.AutoSlugField(null=True, populate_from=b'title', editable=False, max_length=100, blank=True, unique=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='tag',
            name='slug',
            field=orb.fields.AutoSlugField(null=True, populate_from=b'name', editable=False, max_length=100, blank=True, unique=True),
            preserve_default=True,
        ),
    ]
