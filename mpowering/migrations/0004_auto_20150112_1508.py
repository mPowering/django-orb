# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mpowering', '0003_auto_20150112_1256'),
    ]

    operations = [
        migrations.CreateModel(
            name='ResourceOrganisation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('create_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('create_user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('organisation', models.ForeignKey(to='mpowering.Organisation')),
                ('resource', models.ForeignKey(to='mpowering.Resource')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterModelOptions(
            name='resource',
            options={'verbose_name': 'Resource', 'verbose_name_plural': 'Resources'},
        ),
        migrations.AddField(
            model_name='organisation',
            name='url',
            field=models.URLField(default=None, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='resourcefile',
            name='description',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='resourceurl',
            name='description',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='resourceurl',
            name='url',
            field=models.URLField(max_length=500),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='tag',
            name='image',
            field=models.ImageField(null=True, upload_to=b'tag', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='tag',
            name='slug',
            field=models.CharField(max_length=100, null=True, blank=True),
            preserve_default=True,
        ),
    ]
