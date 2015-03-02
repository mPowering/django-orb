# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mpowering', '0015_tag_parent_tag'),
    ]

    operations = [
        migrations.AddField(
            model_name='resourcefile',
            name='file_full_text',
            field=models.TextField(default=None, null=True, blank=True),
            preserve_default=True,
        ),
    ]
