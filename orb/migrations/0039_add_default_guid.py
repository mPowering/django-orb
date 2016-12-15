# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('orb', '0038_add_guid_values'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resource',
            name='guid',
            field=models.UUIDField(default=uuid.uuid4, unique=True, null=True, editable=False),
        ),
        migrations.AlterField(
            model_name='resourcefile',
            name='guid',
            field=models.UUIDField(default=uuid.uuid4, unique=True, null=True, editable=False),
        ),
        migrations.AlterField(
            model_name='resourceurl',
            name='guid',
            field=models.UUIDField(default=uuid.uuid4, unique=True, null=True, editable=False),
        ),
    ]
