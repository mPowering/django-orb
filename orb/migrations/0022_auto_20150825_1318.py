# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('orb', '0021_tagproperty'),
    ]

    operations = [
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.TextField()),
                ('description', models.TextField(default=None, null=True, blank=True)),
                ('visibility', models.CharField(default=b'private', max_length=50, choices=[(b'public', 'Public'), (b'private', 'Private')])),
                ('image', models.ImageField(null=True, upload_to=b'collection/%Y/%m/%d', blank=True)),
                ('slug', models.CharField(max_length=500, null=True, blank=True)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ('title',),
                'verbose_name': 'Collection',
                'verbose_name_plural': 'Collections',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CollectionResource',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order_by', models.IntegerField(default=0)),
                ('collection', models.ForeignKey(to='orb.Collection')),
                ('resource', models.ForeignKey(to='orb.Resource')),
            ],
            options={
                'ordering': ('collection', 'order_by', 'resource'),
                'verbose_name': 'Collection resource',
                'verbose_name_plural': 'Collection resources',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CollectionUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('collection', models.ForeignKey(to='orb.Collection')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('collection', 'user'),
                'verbose_name': 'Collection user',
                'verbose_name_plural': 'Collection users',
            },
            bases=(models.Model,),
        ),
        migrations.AlterModelOptions(
            name='tagproperty',
            options={'ordering': ('tag', 'name', 'value'), 'verbose_name': 'Tag property', 'verbose_name_plural': 'Tag properties'},
        ),
    ]
