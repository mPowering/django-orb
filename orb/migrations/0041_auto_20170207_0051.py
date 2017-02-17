# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orb', '0040_add_tracking_fields'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resource',
            name='source_url',
            field=models.URLField(help_text='Original resource URL.', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='tag',
            name='name_en',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='tag',
            name='name_es',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='tag',
            name='name_pt_br',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterUniqueTogether(
            name='tag',
            unique_together=set([('name', 'category')]),
        ),
    ]
