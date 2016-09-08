# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orb', '0030_auto_20160907_1547'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(unique=True, max_length=100),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='tag',
            name='name_en',
            field=models.CharField(max_length=100, unique=True, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='tag',
            name='name_es',
            field=models.CharField(max_length=100, unique=True, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='tag',
            name='name_pt_br',
            field=models.CharField(max_length=100, unique=True, null=True),
            preserve_default=True,
        ),
    ]
