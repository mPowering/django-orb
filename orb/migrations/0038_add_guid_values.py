# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import uuid

from django.db import migrations


def add_guid_values(apps, schema_editor):
    for classname in ["Resource", "ResourceFile", "ResourceURL"]:
        modelclass = apps.get_model("orb", classname)
        for instance in modelclass.objects.all():
            instance.guid = uuid.uuid4()
            instance.save()


class Migration(migrations.Migration):

    dependencies = [
        ('orb', '0037_resource_guid_field'),
    ]

    operations = [
        migrations.RunPython(add_guid_values),
    ]
