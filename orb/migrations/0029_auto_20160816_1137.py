# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orb', '0028_merge'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='resourcecriteria',
            options={'verbose_name': 'resource criterion', 'verbose_name_plural': 'resource criteria'},
        ),
        migrations.AlterModelOptions(
            name='userprofile',
            options={'verbose_name': 'user profile', 'verbose_name_plural': 'user profiles'},
        ),
        migrations.AlterField(
            model_name='reviewerrole',
            name='name',
            field=models.CharField(default=b'medical', unique=True, max_length=100, choices=[(b'medical', 'Medical'), (b'technical', 'Technical'), (b'training', 'Training')]),
            preserve_default=True,
        ),
    ]
