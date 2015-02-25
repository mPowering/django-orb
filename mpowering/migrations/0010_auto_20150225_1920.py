# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mpowering', '0009_auto_20150220_1644'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='organisation',
            name='create_user',
        ),
        migrations.RemoveField(
            model_name='organisation',
            name='update_user',
        ),
        migrations.RemoveField(
            model_name='resourceorganisation',
            name='create_user',
        ),
        migrations.RemoveField(
            model_name='resourceorganisation',
            name='organisation',
        ),
        migrations.RemoveField(
            model_name='resourceorganisation',
            name='resource',
        ),
        migrations.DeleteModel(
            name='ResourceOrganisation',
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='organisation',
            field=models.ForeignKey(to='mpowering.Tag'),
            preserve_default=True,
        ),
        migrations.DeleteModel(
            name='Organisation',
        ),
    ]
