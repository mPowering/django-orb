# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mpowering', '0013_auto_20150228_1452'),
    ]

    operations = [
        migrations.RenameField(
            model_name='resourcefile',
            old_name='summary',
            new_name='title',
        ),
        migrations.RenameField(
            model_name='resourceurl',
            old_name='summary',
            new_name='title',
        ),
    ]
