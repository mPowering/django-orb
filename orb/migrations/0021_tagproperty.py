# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orb', '0020_auto_20150707_1245'),
    ]

    operations = [
        migrations.CreateModel(
            name='TagProperty',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.TextField()),
                ('value', models.TextField()),
                ('tag', models.ForeignKey(to='orb.Tag')),
            ],
            options={
                'ordering': ('name', 'value'),
                'verbose_name': 'TagProperty',
                'verbose_name_plural': 'TagProperties',
            },
            bases=(models.Model,),
        ),
    ]
