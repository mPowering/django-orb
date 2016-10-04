# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orb', '0031_auto_20160909_1450'),
    ]

    operations = [
        migrations.AddField(
            model_name='resourcecriteria',
            name='role',
            field=models.ForeignKey(related_name='criteria', blank=True, to='orb.ReviewerRole', help_text='Used to show specific criteria to reviewers based on their role. Leave blank if criterion applies generally.', null=True),
            preserve_default=True,
        ),
    ]
