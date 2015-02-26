# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mpowering', '0011_tag_summary'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tag',
            old_name='descripition',
            new_name='description',
        ),
    ]
