# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('OnemCHW', '0002_auto_20151013_1705'),
    ]

    operations = [
        migrations.AddField(
            model_name='countrydata',
            name='last_census_year',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='countrydata',
            name='create_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 13, 17, 25, 38, 654393, tzinfo=utc), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='countrydata',
            name='update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 13, 17, 25, 38, 654431, tzinfo=utc), auto_now=True),
            preserve_default=True,
        ),
    ]
