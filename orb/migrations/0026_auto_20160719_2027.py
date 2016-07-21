# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orb', '0025_specify_profile_db_table'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReviewerRole',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=100, choices=[(b'medical', 'Medical'), (b'technical', 'Technical'), (b'other', 'Other')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='reviewer_role',
            field=models.ForeignKey(blank=True, to='orb.ReviewerRole', null=True),
            preserve_default=True,
        ),
    ]
