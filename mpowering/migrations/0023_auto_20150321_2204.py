# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mpowering', '0022_auto_20150321_1939'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='tagowner',
            unique_together=set([('user', 'tag')]),
        ),
    ]
