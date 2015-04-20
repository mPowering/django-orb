# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('orb', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ResourceWorkflowTracker',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(max_length=50, choices=[(b'rejected', 'Rejected'), (b'pending_mep', 'Pending MEP'), (b'approved', 'Approved')])),
                ('notes', models.TextField(null=True, blank=True)),
                ('owner_email_sent', models.BooleanField(default=False)),
                ('create_user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('resource', models.ForeignKey(to='orb.Resource')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
