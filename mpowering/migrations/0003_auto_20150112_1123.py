# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mpowering', '0002_resourcerelationship'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.TextField()),
                ('slug', models.TextField()),
                ('top_level', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ResourceTag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('create_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('create_user', models.ForeignKey(related_name='resourcetag_create_user', to=settings.AUTH_USER_MODEL)),
                ('resource', models.ForeignKey(to='mpowering.Resource')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.TextField()),
                ('create_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('update_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('category', models.ForeignKey(to='mpowering.Category')),
                ('create_user', models.ForeignKey(related_name='tag_create_user', to=settings.AUTH_USER_MODEL)),
                ('update_user', models.ForeignKey(related_name='tag_update_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='resourcetag',
            name='tag',
            field=models.ForeignKey(to='mpowering.Tag'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='resourcerelationship',
            name='relationship_type',
            field=models.CharField(max_length=50, choices=[(b'is_translation_of', 'is translation of'), (b'is_derivative_of', 'is derivative of'), (b'is_contained_in', 'is contained in')]),
            preserve_default=True,
        ),
    ]
