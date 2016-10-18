# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='contentreview',
            unique_together=set([('resource', 'role')]),
        ),
    ]
