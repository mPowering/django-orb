# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orb', '0032_resourcecriteria_role'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='reviewer_role',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='reviewer_roles',
            field=models.ManyToManyField(to='orb.ReviewerRole', blank=True),
            preserve_default=True,
        ),
    ]
