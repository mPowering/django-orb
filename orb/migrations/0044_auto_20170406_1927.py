# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orb', '0043_tag_published'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='resourcetag',
            options={'ordering': ('id',)},
        ),
        migrations.AlterField(
            model_name='collection',
            name='description',
            field=models.TextField(default=None, help_text='A description of the collection', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='collection',
            name='title',
            field=models.TextField(help_text='A title for the collection'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='parent_tag',
            field=models.ForeignKey(related_name='children', default=None, blank=True, to='orb.Tag', null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='crt_member',
            field=models.BooleanField(default=False, help_text='deprecated'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='mep_member',
            field=models.BooleanField(default=False, help_text='deprecated'),
        ),
    ]
