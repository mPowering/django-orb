# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('orb', '0009_auto_20150504_1403'),
    ]

    operations = [
        migrations.CreateModel(
            name='TagTracker',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(default=b'view', max_length=50, choices=[(b'view', 'View'), (b'view-api', 'View-api')])),
                ('access_date', models.DateTimeField(auto_now_add=True)),
                ('ip', models.IPAddressField(default=None, null=True, blank=True)),
                ('user_agent', models.TextField(default=None, null=True, blank=True)),
                ('extra_data', models.TextField(default=None, null=True, blank=True)),
                ('tag', models.ForeignKey(default=None, blank=True, to='orb.Tag', null=True)),
                ('user', models.ForeignKey(default=None, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
