# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('peers', '0001_initial'),
        ('orb', '0039_add_default_guid'),
    ]

    operations = [
        migrations.AddField(
            model_name='resource',
            name='source_host',
            field=models.URLField(help_text='Host URL of the original ORB instance where resource was sourced.', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='resource',
            name='source_name',
            field=models.CharField(help_text='Name of the source ORB instance where resource was sourced.', max_length=200, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='resource',
            name='source_peer',
            field=models.ForeignKey(related_name='resources', blank=True, to='peers.Peer', help_text='The peer ORB from which the resource was downloaded.', null=True),
        ),
        migrations.AddField(
            model_name='resource',
            name='source_url',
            field=models.URLField(help_text='Original resource URL', null=True, blank=True),
        ),
    ]
