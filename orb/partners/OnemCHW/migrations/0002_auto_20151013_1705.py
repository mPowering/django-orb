# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('OnemCHW', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='countrydata',
            name='create_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 13, 17, 5, 0, 50452, tzinfo=utc), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='countrydata',
            name='update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 13, 17, 5, 0, 50490, tzinfo=utc), auto_now=True),
            preserve_default=True,
        ),
    ]
