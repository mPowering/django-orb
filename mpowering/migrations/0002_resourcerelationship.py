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
            name='ResourceRelationship',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('relationship_type', models.CharField(max_length=50, choices=[(b'is_translation_of', 'is translation of'), (b'is_used_by', 'is used by'), (b'is_contained_in', 'is contained in')])),
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
    ]
