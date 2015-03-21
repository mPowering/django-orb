# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mpowering', '0021_auto_20150321_0758'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='resourcetag',
            unique_together=set([('resource', 'tag')]),
        ),
    ]
