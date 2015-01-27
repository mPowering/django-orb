# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mpowering', '0003_auto_20150127_1450'),
    ]

    operations = [
        migrations.CreateModel(
            name='ResourceTracker',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(max_length=50, choices=[(b'view', 'View'), (b'edit', 'Edit'), (b'download', 'Download'), (b'create', 'Create')])),
                ('access_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('ip', models.IPAddressField(default=None, null=True, blank=True)),
                ('user_agent', models.TextField(default=None, null=True, blank=True)),
                ('extra_data', models.TextField(default=None, null=True, blank=True)),
                ('resource', models.ForeignKey(default=None, blank=True, to='mpowering.Resource', null=True)),
                ('resource_file', models.ForeignKey(default=None, blank=True, to='mpowering.ResourceFile', null=True)),
                ('resource_url', models.ForeignKey(default=None, blank=True, to='mpowering.ResourceURL', null=True)),
                ('user', models.ForeignKey(default=None, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SearchTracker',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('query', models.TextField(default=None, null=True, blank=True)),
                ('no_results', models.IntegerField(default=0, null=True, blank=True)),
                ('access_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('ip', models.IPAddressField(default=None, null=True, blank=True)),
                ('user_agent', models.TextField(default=None, null=True, blank=True)),
                ('user', models.ForeignKey(default=None, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='tracker',
            name='resource',
        ),
        migrations.RemoveField(
            model_name='tracker',
            name='resource_file',
        ),
        migrations.RemoveField(
            model_name='tracker',
            name='resource_url',
        ),
        migrations.RemoveField(
            model_name='tracker',
            name='user',
        ),
        migrations.DeleteModel(
            name='Tracker',
        ),
    ]
