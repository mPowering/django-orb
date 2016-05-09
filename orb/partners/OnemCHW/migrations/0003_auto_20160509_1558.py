# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import orb.fields


class Migration(migrations.Migration):

    dependencies = [
        ('OnemCHW', '0002_auto_20151028_2050'),
    ]

    operations = [
        migrations.AlterField(
            model_name='countrydata',
            name='slug',
            field=orb.fields.AutoSlugField(null=True, populate_from=b'country_name', editable=False, max_length=100, blank=True, unique=True),
            preserve_default=True,
        ),
    ]
