# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orb', '0034_auto_20161004_2145'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resource',
            name='status',
            field=models.CharField(default=b'pending_crt', max_length=50, choices=[(b'rejected', 'Rejected'), (b'pending_crt', 'Pending'), (b'pending_mrt', 'Pending'), (b'approved', 'Approved')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='resourceworkflowtracker',
            name='status',
            field=models.CharField(default=b'pending_crt', max_length=50, choices=[(b'rejected', 'Rejected'), (b'pending_crt', 'Pending'), (b'pending_mrt', 'Pending'), (b'approved', 'Approved')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='reviewer_roles',
            field=models.ManyToManyField(related_name='profiles', to='orb.ReviewerRole', blank=True),
            preserve_default=True,
        ),
    ]
