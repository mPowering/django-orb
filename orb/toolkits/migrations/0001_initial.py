# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Toolkit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order_by', models.IntegerField(default=0)),
                ('title', models.CharField(max_length=200)),
                ('title_en', models.CharField(max_length=200, null=True)),
                ('title_es', models.CharField(max_length=200, null=True)),
                ('title_pt_br', models.CharField(max_length=200, null=True)),
                ('url', models.URLField()),
                ('description', tinymce.models.HTMLField()),
                ('description_en', tinymce.models.HTMLField(null=True)),
                ('description_es', tinymce.models.HTMLField(null=True)),
                ('description_pt_br', tinymce.models.HTMLField(null=True)),
                ('uploaded_image', models.ImageField(null=True, upload_to=b'', blank=True)),
                ('external_image', models.CharField(max_length=1000, null=True, blank=True)),
            ],
            options={
                'ordering': ('order_by',),
                'verbose_name': 'toolkit',
                'verbose_name_plural': 'toolkits',
            },
        ),
    ]
