# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CountryData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('country_name', models.TextField()),
                ('slug', models.CharField(max_length=100, null=True, blank=True)),
                ('country_code', models.TextField()),
                ('no_children_under5', models.BigIntegerField(null=True, blank=True)),
                ('no_chw', models.BigIntegerField(null=True, blank=True)),
                ('pop_est', models.BigIntegerField(null=True, blank=True)),
                ('no_childbearing_age', models.BigIntegerField(null=True, blank=True)),
                ('fertility_rate', models.DecimalField(null=True, max_digits=6, decimal_places=2, blank=True)),
                ('under5_mortality', models.IntegerField(null=True, blank=True)),
                ('last_census_year', models.IntegerField(null=True, blank=True)),
                ('create_date', models.DateTimeField(default=datetime.datetime(2015, 10, 27, 21, 9, 13, 761625, tzinfo=utc), auto_now_add=True)),
                ('update_date', models.DateTimeField(default=datetime.datetime(2015, 10, 27, 21, 9, 13, 761666, tzinfo=utc), auto_now=True)),
            ],
            options={
                'ordering': ('country_name',),
                'verbose_name': 'CountryData',
                'verbose_name_plural': 'CountryData',
            },
            bases=(models.Model,),
        ),
    ]
