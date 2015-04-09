# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mpowering', '0023_auto_20150321_2204'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='age_range',
            field=models.CharField(default=b'none', max_length=50, choices=[(b'under_18', 'under 18'), (b'18_25', '18-25'), (b'25_35', '25-35'), (b'35_50', '35-50'), (b'over_50', 'over 50'), (b'none', 'Prefer not to say')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='gender',
            field=models.CharField(default=b'none', max_length=50, choices=[(b'male', 'Male'), (b'female', 'Female'), (b'none', 'Prefer not to say')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='mailing',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='role',
            field=models.ForeignKey(related_name='role', default=None, blank=True, to='mpowering.Tag', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='organisation',
            field=models.ForeignKey(related_name='organisation', to='mpowering.Tag'),
            preserve_default=True,
        ),
    ]
