# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    replaces = [(b'mpowering', '0001_initial'), (b'mpowering', '0002_tracker'), (b'mpowering', '0003_auto_20150127_1450'), (b'mpowering', '0004_auto_20150127_1612'), (b'mpowering', '0005_auto_20150127_1723'), (b'mpowering', '0006_resourcerating'), (b'mpowering', '0007_auto_20150203_1949'), (b'mpowering', '0008_auto_20150206_1158'), (b'mpowering', '0009_auto_20150220_1644'), (b'mpowering', '0010_auto_20150225_1920'), (b'mpowering', '0011_tag_summary'), (b'mpowering', '0012_auto_20150226_1106'), (b'mpowering', '0013_auto_20150228_1452'), (b'mpowering', '0014_auto_20150228_1454'), (b'mpowering', '0015_tag_parent_tag'), (b'mpowering', '0016_resourcefile_file_full_text'), (b'mpowering', '0017_auto_20150315_1440'), (b'mpowering', '0018_auto_20150316_1613'), (b'mpowering', '0019_resource_born_on'), (b'mpowering', '0020_tagowner'), (b'mpowering', '0021_auto_20150321_0758'), (b'mpowering', '0022_auto_20150321_1939'), (b'mpowering', '0023_auto_20150321_2204'), (b'mpowering', '0024_auto_20150409_0218')]

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
                ('status', models.CharField(max_length=50, choices=[(b'rejected', 'Rejected'), (b'pending', 'Pending'), (b'approved', 'Approved')])),
                ('create_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('update_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('slug', models.CharField(max_length=100, null=True, blank=True)),
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
                ('description', models.TextField(null=True, blank=True)),
                ('create_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('update_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('create_user', models.ForeignKey(related_name='resource_file_create_user', to=settings.AUTH_USER_MODEL)),
                ('resource', models.ForeignKey(to='mpowering.Resource')),
                ('update_user', models.ForeignKey(related_name='resource_file_update_user', to=settings.AUTH_USER_MODEL)),
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
                ('resource', models.ForeignKey(related_name='resource', to='mpowering.Resource')),
                ('resource_related', models.ForeignKey(related_name='resource_related', to='mpowering.Resource')),
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
                ('create_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('create_user', models.ForeignKey(related_name='resourcetag_create_user', to=settings.AUTH_USER_MODEL)),
                ('resource', models.ForeignKey(to='mpowering.Resource')),
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
                ('description', models.TextField(null=True, blank=True)),
                ('create_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('update_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('create_user', models.ForeignKey(related_name='resource_url_create_user', to=settings.AUTH_USER_MODEL)),
                ('resource', models.ForeignKey(to='mpowering.Resource')),
                ('update_user', models.ForeignKey(related_name='resource_url_update_user', to=settings.AUTH_USER_MODEL)),
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
                ('category', models.ForeignKey(to='mpowering.Category')),
                ('create_user', models.ForeignKey(related_name='tag_create_user', to=settings.AUTH_USER_MODEL)),
                ('update_user', models.ForeignKey(related_name='tag_update_user', to=settings.AUTH_USER_MODEL)),
                ('description', models.TextField(default=None, null=True, blank=True)),
                ('external_url', models.URLField(default=None, max_length=500, null=True, blank=True)),
                ('summary', models.CharField(max_length=100, null=True, blank=True)),
                ('parent_tag', models.ForeignKey(default=None, blank=True, to='mpowering.Tag', null=True)),
            ],
            options={
                'verbose_name': 'Tag',
                'verbose_name_plural': 'Tags',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('about', models.TextField(default=None, null=True, blank=True)),
                ('job_title', models.TextField(default=None, null=True, blank=True)),
                ('phone_number', models.TextField(default=None, null=True, blank=True)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('organisation', models.ForeignKey(to='mpowering.Tag')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
                ('api_access', models.BooleanField(default=False)),
                ('age_range', models.CharField(default=b'none', max_length=50, choices=[(b'under_18', 'under 18'), (b'18_25', '18-25'), (b'25_35', '25-35'), (b'35_50', '35-50'), (b'over_50', 'over 50'), (b'none', 'Prefer not to say')])),
                ('gender', models.CharField(default=b'none', max_length=50, choices=[(b'male', 'Male'), (b'female', 'Female'), (b'none', 'Prefer not to say')])),
                ('mailing', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='resourcetag',
            name='tag',
            field=models.ForeignKey(to='mpowering.Tag'),
            preserve_default=True,
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
                ('resource', models.ForeignKey(default=None, blank=True, to='mpowering.Resource', null=True)),
                ('resource_file', models.ForeignKey(default=None, blank=True, to='mpowering.ResourceFile', null=True)),
                ('resource_url', models.ForeignKey(default=None, blank=True, to='mpowering.ResourceURL', null=True)),
                ('user', models.ForeignKey(default=None, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
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
                ('user', models.ForeignKey(default=None, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('type', models.CharField(default=b'search', max_length=50, choices=[(b'search', 'search'), (b'search-api', 'search-api')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='resource',
            name='create_date',
            field=models.DateTimeField(auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='resource',
            name='update_date',
            field=models.DateTimeField(auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='resourcefile',
            name='create_date',
            field=models.DateTimeField(auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='resourcefile',
            name='update_date',
            field=models.DateTimeField(auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='resourcetag',
            name='create_date',
            field=models.DateTimeField(auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='resourceurl',
            name='create_date',
            field=models.DateTimeField(auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='resourceurl',
            name='update_date',
            field=models.DateTimeField(auto_now=True),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='ResourceRating',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('rating', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('comments', models.TextField(default=None, null=True, blank=True)),
                ('resource', models.ForeignKey(to='mpowering.Resource')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='resource',
            name='status',
            field=models.CharField(max_length=50, choices=[(b'rejected', 'Rejected'), (b'pending_crt', 'Pending CRT'), (b'pending_mrt', 'Pending MRT'), (b'approved', 'Approved')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='resourcefile',
            name='title',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='resourceurl',
            name='title',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='resourcefile',
            name='file_full_text',
            field=models.TextField(default=None, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='resource',
            name='status',
            field=models.CharField(default=b'pending_crt', max_length=50, choices=[(b'rejected', 'Rejected'), (b'pending_crt', 'Pending CRT'), (b'pending_mrt', 'Pending MRT'), (b'approved', 'Approved')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='resource',
            name='study_time_number',
            field=models.IntegerField(default=0, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='resource',
            name='study_time_unit',
            field=models.CharField(blank=True, max_length=10, null=True, choices=[(b'mins', 'Mins'), (b'hours', 'Hours'), (b'days', 'Days'), (b'weeks', 'Weeks')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='resource',
            name='born_on',
            field=models.DateTimeField(default=None, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='TagOwner',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tag', models.ForeignKey(to='mpowering.Tag')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='resourcetag',
            unique_together=set([('resource', 'tag')]),
        ),
        migrations.AlterUniqueTogether(
            name='tagowner',
            unique_together=set([('user', 'tag')]),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='role',
            field=models.ForeignKey(related_name='role', default=None, blank=True, to='mpowering.Tag', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='organisation',
            field=models.ForeignKey(related_name='organisation', to='mpowering.Tag'),
            preserve_default=True,
        ),
    ]
