# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mpowering', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tracker',
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
    ]
