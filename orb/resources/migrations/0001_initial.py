# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import model_utils.fields
import django.utils.timezone
from django.conf import settings
import django_fsm


class Migration(migrations.Migration):

    dependencies = [
        ('orb', '0025_specify_profile_db_table'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ContentReview',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('status', django_fsm.FSMField(default=b'pending_crt', max_length=50)),
                ('notes', models.TextField(blank=True)),
                ('role', models.CharField(max_length=10, choices=[(b'medical', 'Medical'), (b'technical', 'Technical'), (b'other', 'Other')])),
                ('resource', models.ForeignKey(related_name='content_reviews', to='orb.Resource')),
                ('reviewer', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ReviewLogEntry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('review_status', models.CharField(max_length=20, editable=False)),
                ('review', models.ForeignKey(related_name='log_entries', to='resources.ContentReview')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
