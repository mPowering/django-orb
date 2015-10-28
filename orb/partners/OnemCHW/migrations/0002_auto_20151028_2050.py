# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('OnemCHW', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='countrydata',
            name='create_date',
            field=models.DateTimeField(auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='countrydata',
            name='update_date',
            field=models.DateTimeField(auto_now=True),
            preserve_default=True,
        ),
    ]
