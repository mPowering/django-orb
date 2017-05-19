# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('top_level', models.BooleanField(default=False)),
                ('slug', models.CharField(max_length=100, null=True, blank=True)),
                ('order_by', models.IntegerField(default=0)),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.TextField()),
                ('description', models.TextField()),
                ('image', models.ImageField(max_length=200, null=True, upload_to=b'resourceimage/%Y/%m/%d', blank=True)),
                ('status', models.CharField(default=b'pending', max_length=50, choices=[(b'rejected', 'Rejected'), (b'pending', 'Pending CRT'), (b'pending_mrt', 'Pending MRT'), (b'approved', 'Approved')])),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('slug', models.CharField(max_length=100, null=True, blank=True)),
                ('study_time_number', models.IntegerField(default=0, null=True, blank=True)),
                ('study_time_unit', models.CharField(blank=True, max_length=10, null=True, choices=[(b'mins', 'Mins'), (b'hours', 'Hours'), (b'days', 'Days'), (b'weeks', 'Weeks')])),
                ('born_on', models.DateTimeField(default=None, null=True, blank=True)),
                ('create_user', models.ForeignKey(related_name='resource_create_user', to=settings.AUTH_USER_MODEL)),
                ('update_user', models.ForeignKey(related_name='resource_update_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Resource',
                'verbose_name_plural': 'Resources',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ResourceFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('file', models.FileField(max_length=200, upload_to=b'resource/%Y/%m/%d')),
                ('title', models.TextField(null=True, blank=True)),
                ('description', models.TextField(null=True, blank=True)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('file_full_text', models.TextField(default=None, null=True, blank=True)),
                ('create_user', models.ForeignKey(related_name='resource_file_create_user', to=settings.AUTH_USER_MODEL)),
                ('resource', models.ForeignKey(to='orb.Resource')),
                ('update_user', models.ForeignKey(related_name='resource_file_update_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ResourceRating',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('rating', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('comments', models.TextField(default=None, null=True, blank=True)),
                ('resource', models.ForeignKey(to='orb.Resource')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ResourceRelationship',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('relationship_type', models.CharField(max_length=50, choices=[(b'is_translation_of', 'is translation of'), (b'is_derivative_of', 'is derivative of'), (b'is_contained_in', 'is contained in')])),
                ('description', models.TextField()),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('create_user', models.ForeignKey(related_name='resource_relationship_create_user', to=settings.AUTH_USER_MODEL)),
                ('resource', models.ForeignKey(related_name='resource', to='orb.Resource')),
                ('resource_related', models.ForeignKey(related_name='resource_related', to='orb.Resource')),
                ('update_user', models.ForeignKey(related_name='resource_relationship_update_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ResourceTag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('create_user', models.ForeignKey(related_name='resourcetag_create_user', to=settings.AUTH_USER_MODEL)),
                ('resource', models.ForeignKey(to='orb.Resource')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ResourceTracker',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(default=b'view', max_length=50, choices=[(b'view', 'View'), (b'view-api', 'View-api'), (b'edit', 'Edit'), (b'download', 'Download'), (b'create', 'Create')])),
                ('access_date', models.DateTimeField(auto_now_add=True)),
                ('ip', models.IPAddressField(default=None, null=True, blank=True)),
                ('user_agent', models.TextField(default=None, null=True, blank=True)),
                ('extra_data', models.TextField(default=None, null=True, blank=True)),
                ('resource', models.ForeignKey(default=None, blank=True, to='orb.Resource', null=True)),
                ('resource_file', models.ForeignKey(default=None, blank=True, to='orb.ResourceFile', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ResourceURL',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.URLField(max_length=500)),
                ('title', models.TextField(null=True, blank=True)),
                ('description', models.TextField(null=True, blank=True)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('create_user', models.ForeignKey(related_name='resource_url_create_user', to=settings.AUTH_USER_MODEL)),
                ('resource', models.ForeignKey(to='orb.Resource')),
                ('update_user', models.ForeignKey(related_name='resource_url_update_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SearchTracker',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('query', models.TextField(default=None, null=True, blank=True)),
                ('no_results', models.IntegerField(default=0, null=True, blank=True)),
                ('access_date', models.DateTimeField(auto_now_add=True)),
                ('ip', models.IPAddressField(default=None, null=True, blank=True)),
                ('user_agent', models.TextField(default=None, null=True, blank=True)),
                ('type', models.CharField(default=b'search', max_length=50, choices=[(b'search', 'search'), (b'search-api', 'search-api')])),
                ('user', models.ForeignKey(default=None, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('image', models.ImageField(null=True, upload_to=b'tag/%Y/%m/%d', blank=True)),
                ('slug', models.CharField(max_length=100, null=True, blank=True)),
                ('order_by', models.IntegerField(default=0)),
                ('external_url', models.URLField(default=None, max_length=500, null=True, blank=True)),
                ('description', models.TextField(default=None, null=True, blank=True)),
                ('summary', models.CharField(max_length=100, null=True, blank=True)),
                ('contact_email', models.CharField(max_length=100, null=True, blank=True)),
                ('category', models.ForeignKey(to='orb.Category')),
                ('create_user', models.ForeignKey(related_name='tag_create_user', to=settings.AUTH_USER_MODEL)),
                ('parent_tag', models.ForeignKey(default=None, blank=True, to='orb.Tag', null=True)),
                ('update_user', models.ForeignKey(related_name='tag_update_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Tag',
                'verbose_name_plural': 'Tags',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TagOwner',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tag', models.ForeignKey(to='orb.Tag')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('about', models.TextField(default=None, null=True, blank=True)),
                ('job_title', models.TextField(default=None, null=True, blank=True)),
                ('role_other', models.TextField(default=None, null=True, blank=True)),
                ('phone_number', models.TextField(default=None, null=True, blank=True)),
                ('api_access', models.BooleanField(default=False)),
                ('gender', models.CharField(default=b'none', max_length=50, choices=[(b'female', 'Female'), (b'male', 'Male'), (b'none', 'Prefer not to say')])),
                ('age_range', models.CharField(default=b'none', max_length=50, choices=[(b'under_18', 'under 18'), (b'18_25', '18-24'), (b'25_35', '25-34'), (b'35_50', '35-50'), (b'over_50', 'over 50'), (b'none', 'Prefer not to say')])),
                ('mailing', models.BooleanField(default=False)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('organisation', models.ForeignKey(related_name='organisation', to='orb.Tag')),
                ('role', models.ForeignKey(related_name='role', default=None, blank=True, to='orb.Tag', null=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='tagowner',
            unique_together=set([('user', 'tag')]),
        ),
        migrations.AddField(
            model_name='resourcetracker',
            name='resource_url',
            field=models.ForeignKey(default=None, blank=True, to='orb.ResourceURL', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='resourcetracker',
            name='user',
            field=models.ForeignKey(default=None, blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='resourcetag',
            name='tag',
            field=models.ForeignKey(to='orb.Tag'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='resourcetag',
            unique_together=set([('resource', 'tag')]),
        ),
    ]
