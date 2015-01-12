# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('top_level', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Organisation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.TextField()),
                ('location', models.TextField(default=None, null=True, blank=True)),
                ('create_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('update_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('create_user', models.ForeignKey(related_name='organisation_create_user', to=settings.AUTH_USER_MODEL)),
                ('update_user', models.ForeignKey(related_name='organisation_update_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.TextField()),
                ('description', models.TextField()),
                ('create_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('update_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('create_user', models.ForeignKey(related_name='resource_create_user', to=settings.AUTH_USER_MODEL)),
                ('update_user', models.ForeignKey(related_name='resource_update_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ResourceFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('file', models.FileField(max_length=200, upload_to=b'mpowering/%Y/%m/%d')),
                ('description', models.TextField()),
                ('create_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('update_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('create_user', models.ForeignKey(related_name='resource_file_create_user', to=settings.AUTH_USER_MODEL)),
                ('resource', models.ForeignKey(to='mpowering.Resource')),
                ('update_user', models.ForeignKey(related_name='resource_file_update_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ResourceRelationship',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('relationship_type', models.CharField(max_length=50, choices=[(b'is_translation_of', 'is translation of'), (b'is_derivative_of', 'is derivative of'), (b'is_contained_in', 'is contained in')])),
                ('description', models.TextField()),
                ('create_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('update_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('create_user', models.ForeignKey(related_name='resource_relationship_create_user', to=settings.AUTH_USER_MODEL)),
                ('resource', models.ForeignKey(related_name='resource', to='mpowering.Resource')),
                ('resource_related', models.ForeignKey(related_name='resource_related', to='mpowering.Resource')),
                ('update_user', models.ForeignKey(related_name='resource_relationship_update_user', to=settings.AUTH_USER_MODEL)),
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
            name='ResourceURL',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.TextField()),
                ('description', models.TextField()),
                ('create_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('update_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('create_user', models.ForeignKey(related_name='resource_url_create_user', to=settings.AUTH_USER_MODEL)),
                ('resource', models.ForeignKey(to='mpowering.Resource')),
                ('update_user', models.ForeignKey(related_name='resource_url_update_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('create_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('update_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('image', models.ImageField(upload_to=b'tag')),
                ('slug', models.CharField(max_length=100)),
                ('category', models.ForeignKey(to='mpowering.Category')),
                ('create_user', models.ForeignKey(related_name='tag_create_user', to=settings.AUTH_USER_MODEL)),
                ('update_user', models.ForeignKey(related_name='tag_update_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('about', models.TextField(default=None, null=True, blank=True)),
                ('job_title', models.TextField(default=None, null=True, blank=True)),
                ('phone_number', models.TextField(default=None, null=True, blank=True)),
                ('create_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('update_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('organisation', models.OneToOneField(to='mpowering.Organisation')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
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
    ]
