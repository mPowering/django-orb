# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mpowering', '0001_squashed_0024_auto_20150409_0218'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='role_other',
            field=models.TextField(default=None, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='age_range',
            field=models.CharField(default=b'none', max_length=50, choices=[(b'under_18', 'under 18'), (b'18_25', '18-24'), (b'25_35', '25-34'), (b'35_50', '35-50'), (b'over_50', 'over 50'), (b'none', 'Prefer not to say')]),
            preserve_default=True,
        ),
    ]
