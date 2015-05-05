# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orb', '0011_auto_20150504_1905'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='organisation',
            field=models.ForeignKey(related_name='organisation', default=None, blank=True, to='orb.Tag', null=True),
            preserve_default=True,
        ),
    ]
