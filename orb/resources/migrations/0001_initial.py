# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django_fsm


class Migration(migrations.Migration):

    dependencies = [
        ('orb', '0026_auto_20160719_2027'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ContentReview',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('status', django_fsm.FSMField(default=b'pending_crt', max_length=50)),
                ('notes', models.TextField(blank=True)),
                ('resource', models.ForeignKey(related_name='content_reviews', to='orb.Resource')),
                ('reviewer', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('role', models.ForeignKey(related_name='reviews', to='orb.ReviewerRole')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ReviewLogEntry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('review_status', models.CharField(max_length=20, editable=False)),
                ('action', models.CharField(max_length=200)),
                ('review', models.ForeignKey(related_name='log_entries', to='resources.ContentReview')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='contentreview',
            unique_together=set([('resource', 'role'), ('resource', 'reviewer')]),
        ),
    ]
