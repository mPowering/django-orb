# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orb', '0026_auto_20160719_2027'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reviewerrole',
            name='name',
            field=models.CharField(default=b'medical', unique=True, max_length=100, choices=[(b'medical', 'Medical'), (b'technical', 'Technical'), (b'other', 'Other')]),
            preserve_default=True,
        ),
    ]
