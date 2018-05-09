from __future__ import unicode_literals

import itertools
import uuid

import os
import parsedatetime as pdt
from django.conf import settings
from django.contrib.auth.models import User
from django.core import urlresolvers
from django.core.urlresolvers import reverse
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Avg, Count
from django.utils.translation import ugettext_lazy as _
from modeltranslation.utils import build_localized_fieldname
from typing import Any
from typing import Dict
from typing import Iterable

from orb import signals
from orb.analytics.models import UserLocationVisualization
from orb.fields import AutoSlugField
from orb.fields import image_cleaner
from orb.profiles.querysets import ProfilesQueryset
from orb.resources.managers import ResourceQueryset, ResourceURLManager, TrackerQueryset
from orb.review.queryset import CriteriaQueryset
from orb.tags.managers import ResourceTagManager, TagQuerySet

cal = pdt.Calendar()


class WorkflowQueryset(models.QuerySet):

    def rejected(self):
        return self.filter(status=Resource.REJECTED)

    def notes(self, delimmiter="\n\n"):
        """Returns a concatenated selection of final workflow notes"""
        return delimmiter.join([r.notes for r in self if r.notes])


class TimestampBase(models.Model):
    """Base class for adding create and update timestamp fields to models"""
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


def pop_fields(input, *fieldnames):
    for field in fieldnames:
        input.pop(field, None)
    return input


class Resource(TimestampBase):
    REJECTED = 'rejected'
    APPROVED = 'approved'
    PENDING = 'pending'
    ARCHIVED = 'archived'

    STATUS_TYPES = (
        (APPROVED, _('Approved')),
        (PENDING, _('Pending')),
        (REJECTED, _('Rejected')),
        (ARCHIVED, _('Archived')),
    )

    MINS = 'mins'
    HOURS = 'hours'
    DAYS = 'days'
    WEEKS = 'weeks'
    STUDY_TIME_UNITS = (
        (MINS, _('Mins')),
        (HOURS, _('Hours')),
        (DAYS, _('Days')),
        (WEEKS, _('Weeks')),
    )

    guid = models.UUIDField(null=True, default=uuid.uuid4, unique=True, editable=False)
    title = models.TextField(blank=False, null=False)
    description = models.TextField(blank=False, null=False)
    image = models.ImageField(upload_to='resourceimage/%Y/%m/%d', max_length=200, blank=True, null=True)
    status = models.CharField(max_length=50, choices=STATUS_TYPES, default=PENDING)
    create_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='resource_create_user', blank=True, null=True, default=None, on_delete=models.SET_NULL)
    update_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='resource_update_user', blank=True, null=True, default=None, on_delete=models.SET_NULL)
    slug = AutoSlugField(populate_from='title', max_length=100, blank=True, null=True)
    study_time_number = models.IntegerField(default=0, null=True, blank=True)
    study_time_unit = models.CharField(max_length=10, choices=STUDY_TIME_UNITS, blank=True, null=True)
    born_on = models.DateTimeField(blank=True, null=True, default=None)
    attribution = models.TextField(blank=True, null=True, default=None)

    # Tracking fields
    source_url = models.URLField(null=True, blank=True, help_text=_(u"Original resource URL."))
    source_name = models.CharField(null=True, blank=True, max_length=200,
                                   help_text=_(u"Name of the source ORB instance where resource was sourced."))
    source_host = models.URLField(null=True, blank=True,
                                   help_text=_(u"Host URL of the original ORB instance where resource was sourced."))
    source_peer = models.ForeignKey('peers.Peer', null=True, blank=True, related_name="resources",
                                    help_text=_(u"The peer ORB from which the resource was downloaded."))
    tags = models.ManyToManyField('Tag', through='ResourceTag', blank=True)

    resources = ResourceQueryset.as_manager()
    objects = ResourceQueryset.as_manager()
    # objects = resources  # alias

    # Fields to strip from API data
    API_EXCLUDED_FIELDS = ['id', 'guid']

    class Meta:
        verbose_name = _(u'Resource')
        verbose_name_plural = _(u'Resources')
        ordering = ('title',)

    def __unicode__(self):
        return self.title

    def save(self, **kwargs):
        """Cleans API submitted images"""
        if self.image and (self.image.name.startswith("http://") or self.image.name.startswith("https://")):
            remote_image_file = self.image.name
        else:
            remote_image_file = None

        super(Resource, self).save(**kwargs)

        if remote_image_file:
            image_cleaner(self, url=remote_image_file)

        return self

    def get_absolute_url(self):
        return urlresolvers.reverse('orb_resource', args=[self.slug])

    def update_from_api(self, api_data):
        """
        Conditionally updates a resource based on API data.

        Args:
            api_data: serialized data from the ORB API describing a resource in detail

        Returns:
            boolean for whether the resource needed updating

        """
        if self.is_local():
            raise LookupError("Cannot update a locally created resource from API data")

        if api_data['guid'] != str(self.guid):
            raise LookupError("API GUID {} does not match local GUID {}".format(api_data['guid'], str(self.guid)))

        updated_time, result = cal.parseDT(api_data.pop('update_date'))
        created_time, result = cal.parseDT(api_data.pop('create_date'))

        if updated_time.date <= self.create_date.date:
            return False

        resource_files = api_data.pop('files', [])
        languages = api_data.pop('languages', [])
        tags = api_data.pop('tags', [])
        resource_urls = api_data.pop('urls', [])
        resource_uri = api_data.pop('resource_uri')
        url = api_data.pop('url')

        for field in self.API_EXCLUDED_FIELDS:
            api_data.pop(field, None)

        import_user = get_import_user()

        cleaned_api_data = clean_api_data(api_data, 'attribution', 'description', 'title')

        for attr, value in cleaned_api_data.iteritems():
            setattr(self, attr, value)

        self.update_user = import_user
        self.save()

        return True

    @classmethod
    def create_from_api(cls, api_data, peer=None):
        """
        Creates a new Resource object and its suite of related content based
        on a dictionary of data as returned from the ORB API

        Args:
            api_data: serialized data from the ORB API describing a resource in detail

        Returns:
            the Resource object created

        """

        resource_files = api_data.pop('files', [])
        languages = api_data.pop('languages', [])
        tags = api_data.pop('tags', [])
        resource_urls = api_data.pop('urls', [])
        resource_uri = api_data.pop('resource_uri')
        url = api_data.pop('url')

        import_user = get_import_user()

        cleaned_api_data = clean_api_data(api_data, 'attribution', 'description', 'title')

        resource = cls.resources.create(
            source_peer=peer,
            create_user=import_user,
            update_user=import_user,
            **cleaned_api_data
        )

        ResourceURL.objects.bulk_create([
            ResourceURL.from_url_data(
                resource,
                clean_api_data(resource_url_data, "description", "title"),
                import_user,
            )
            for resource_url_data in resource_urls
        ] + [
            ResourceURL.from_file_data(
                resource,
                clean_api_data(resource_file_data, "description", "title"),
                import_user,
            )
            for resource_file_data in resource_files
        ])

        for tag_data in tags:
            ResourceTag.create_from_api_data(
                resource,
                clean_api_data(tag_data['tag'], "category", "description", "name", "summary"),
                user=import_user,
            )

        return resource

    def approve(self):
        self.status = self.APPROVED
        self.content_reviews.all().update(status=self.APPROVED)
        signals.resource_approved.send(sender=self, resource=self)

    def reject(self):
        self.status = self.REJECTED
        self.content_reviews.all().update(status=self.REJECTED)
        signals.resource_rejected.send(sender=self, resource=self)

    def is_pending(self):
        return self.status not in [self.REJECTED, self.APPROVED]

    def is_local(self):
        return not bool(self.source_peer)

    def has_assignments(self):
        """Returns whether there are *any* reivew assignments"""
        return self.content_reviews.all().exists()

    def get_organisations(self):
        return Tag.objects.filter(resourcetag__resource=self, category__slug='organisation')

    def get_files(self):
        return ResourceFile.objects.filter(resource=self).order_by('order_by')

    def get_urls(self):
        return ResourceURL.objects.filter(resource=self).order_by('order_by')

    def get_categories(self):
        categories = Category.objects.filter(
            tag__resourcetag__resource=self).distinct().order_by('order_by')
        for c in categories:
            c.tags = Tag.objects.filter(resourcetag__resource=self, category=c)
        return categories

    def get_display_categories(self):
        categories = Category.objects.filter(tag__resourcetag__resource=self).exclude(
            slug='license').distinct().order_by('order_by')
        for c in categories:
            c.tags = Tag.tags.filter(category=c).by_resource(self)
        return categories

    def get_category(self, category_slug):
        tags = Tag.objects.filter(
            resourcetag__resource=self, category__slug=category_slug)
        return tags

    def get_type_tags(self):
        tags = Tag.objects.filter(
            resourcetag__resource=self, category__slug='type')
        return tags

    def get_no_hits(self):
        anon = ResourceTracker.objects.filter(resource=self, user=None).values_list('ip',
                                                                                    flat=True).distinct().count()
        identified = ResourceTracker.objects.filter(resource=self).exclude(user=None).values_list('user',
                                                                                                  flat=True).distinct().count()
        return anon + identified

    def get_geographies(self):
        return Tag.tags.by_category('geography').by_resource(self)

    def get_devices(self):
        return Tag.tags.by_category('device').by_resource(self)

    def get_languages(self):
        return Tag.tags.by_category('language').by_resource(self)

    def get_license(self):
        return Tag.tags.by_category('license').by_resource(self)

    def get_health_domains(self):
        return Tag.tags.by_category('health-domain').by_resource(self)

    def get_rating(self):
        rating = ResourceRating.objects.filter(resource=self).aggregate(
            rating=Avg('rating'), count=Count('rating'))
        if rating['rating']:
            rating['rating'] = round(rating['rating'], 0)
        return rating

    def available_languages(self):
        """
        Returns a list of site languages for which this resource has translations

        This is based on having both title and description for these fields.
        """
        field_names = {
            language[0]: [build_localized_fieldname(field, language[0]) for field in ["title", "description"]]
            for language in settings.LANGUAGES
        }

        return [
            language for language, fields in field_names.items() if all([getattr(self, field) for field in fields])
        ]

    def user_can_view(self, user):
        if self.status == Resource.APPROVED:
            return True
        elif user.is_anonymous():
            return False
        elif ((user.is_staff or
                       user == self.create_user or
                       user == self.update_user) or
                  (user.userprofile and (user.userprofile.is_reviewer))):
            return True
        else:
            return False


class ResourceWorkflowTracker(models.Model):
    create_date = models.DateTimeField(auto_now_add=True)
    resource = models.ForeignKey(Resource, blank=True, null=True,
                                 related_name="workflow_trackers")
    create_user = models.ForeignKey(settings.AUTH_USER_MODEL)
    status = models.CharField(
        max_length=50, choices=Resource.STATUS_TYPES, default=Resource.PENDING)
    notes = models.TextField(blank=True, null=True)
    owner_email_sent = models.BooleanField(default=False, blank=False)

    workflows = WorkflowQueryset.as_manager()
    objects = WorkflowQueryset.as_manager()
    # objects = workflows  # Backwards compatible alias


class ResourceURL(TimestampBase):
    guid = models.UUIDField(null=True, default=uuid.uuid4, unique=True, editable=False)
    url = models.URLField(blank=False, null=False, max_length=500)
    resource = models.ForeignKey(Resource)
    title = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    order_by = models.IntegerField(default=0)
    file_size = models.IntegerField(default=0)
    image = models.ImageField(
        upload_to='resourceimage/%Y/%m/%d', max_length=200, blank=True, null=True)
    create_user = models.ForeignKey(User, related_name='resource_url_create_user', blank=True, null=True, default=None, on_delete=models.SET_NULL)
    update_user = models.ForeignKey(User, related_name='resource_url_update_user', blank=True, null=True, default=None, on_delete=models.SET_NULL)

    objects = ResourceURLManager.as_manager()

    def __unicode__(self):
        return self.url

    def get_absolute_url(self):
        return reverse('orb_resource_view_link', kwargs={'id': self.id})

    @classmethod
    def from_url_data(cls, resource, api_data, user=None):
        """
        Creates a new Resource object and its suite of related content based
        on a dictionary of data as returned from the ORB API

        Args:
            resource: associated resource
            api_data: serialized data from the ORB API describing a resource in detail
            user: create_user/update_user

        Returns:
            the ResourceURL object (not saved to DB)

        """
        for field in ['id', 'resource_uri']:
            api_data.pop(field, None)

        if not user:
            user = get_import_user()

        return cls(resource=resource, create_user=user, update_user=user, **api_data)

    @classmethod
    def from_file_data(cls, resource, api_data, user=None):
        """
        Creates a new Resource object and its suite of related content based
        on a dictionary of Resource file data as returned from the ORB API

        Args:
            resource: associated resource
            api_data: serialized data from the ORB API describing a resource in detail
            user: create_user/update_user

        Returns:
            the ResourceURL object (not saved to DB)

        """
        for field in ['id', 'resource_uri']:
            api_data.pop(field, None)

        api_data['url'] = api_data.pop('file')

        if not user:
            user = get_import_user()

        return cls(resource=resource, create_user=user, update_user=user, **api_data)


class ResourceFile(TimestampBase):
    guid = models.UUIDField(null=True, default=uuid.uuid4, unique=True, editable=False)
    file = models.FileField(upload_to='resource/%Y/%m/%d', max_length=200)
    resource = models.ForeignKey(Resource)
    title = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    order_by = models.IntegerField(default=0)
    image = models.ImageField(
        upload_to='resourceimage/%Y/%m/%d', max_length=200, blank=True, null=True)
    create_user = models.ForeignKey(User, related_name='resource_file_create_user', blank=True, null=True, default=None, on_delete=models.SET_NULL)
    update_user = models.ForeignKey(User, related_name='resource_file_update_user', blank=True, null=True, default=None, on_delete=models.SET_NULL)
    file_full_text = models.TextField(blank=True, null=True, default=None)
    objects = ResourceURLManager.as_manager()

    def __unicode__(self):
        return self.title or self.file.name

    def get_absolute_url(self):
        return reverse('orb_resource_view_file', kwargs={'id': self.id})

    def filename(self):
        return os.path.basename(self.file.name)

    @property
    def full_path(self):
        """Returns the complete path to the file"""
        return os.path.join(settings.MEDIA_ROOT, self.file.name)

    @property
    def web_path(self):
        """Returns the relative URL to the file"""
        return settings.MEDIA_URL + self.file.name

    def filesize(self):
        if os.path.isfile(self.full_path):
            return os.path.getsize(self.full_path)
        else:
            return 0

# ResourceRelationship


class ResourceRelationship(TimestampBase):
    RELATIONSHIP_TYPES = (
        ('is_translation_of', _('is translation of')),
        ('is_derivative_of', _('is derivative of')),
        ('is_contained_in', _('is contained in')),
    )

    resource = models.ForeignKey(Resource, related_name='resource')
    resource_related = models.ForeignKey(
        Resource, related_name='resource_related')
    relationship_type = models.CharField(
        max_length=50, choices=RELATIONSHIP_TYPES)
    description = models.TextField(blank=False, null=False)
    create_user = models.ForeignKey(User, related_name='resource_relationship_create_user', blank=True, null=True, default=None, on_delete=models.SET_NULL)
    update_user = models.ForeignKey(User, related_name='resource_relationship_update_user', blank=True, null=True, default=None, on_delete=models.SET_NULL)


class ResourceCriteria(models.Model):
    CATEGORIES = (
        ('qa', _('Quality Assurance')),
        ('value', _('Value for Frontline Health Workers (FLHW)')),
        ('video', _('Video resources')),
        ('animation', _('Animation resources')),
        ('audio', _('Audio resources')),
        ('text', _('Text based resources')),
    )
    description = models.TextField()
    category = models.CharField(max_length=50,
                                choices=CATEGORIES,
                                null=True,
                                blank=True,
                                help_text=_("deprecated"))
    order_by = models.IntegerField(default=0)
    category_order_by = models.IntegerField(default=0,
                                            help_text=_("deprecated"))
    role = models.ForeignKey(
        'orb.ReviewerRole',
        related_name="criteria",
        blank=True, null=True,
        help_text=_(u"Used to show specific criteria to reviewers based on their role. "
                    u"Leave blank if criterion applies generally."),
    )

    criteria = CriteriaQueryset.as_manager()
    objects = CriteriaQueryset.as_manager()
    # objects = criteria

    def get_role_display(self):
        """Returns an appropriate label for the admin"""
        return _("General") if not self.role else self.role.name
    get_role_display.short_description = "Role"

    def __unicode__(self):
        return self.description

    class Meta:
        verbose_name = _("resource criterion")
        verbose_name_plural = _("resource criteria")


class Category(models.Model):
    name = models.CharField(max_length=100)
    top_level = models.BooleanField(default=False)
    slug = AutoSlugField(populate_from='name', max_length=100, blank=True, null=True)
    order_by = models.IntegerField(default=0)

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
        ordering = ('name',)

    def __unicode__(self):
        return self.name

    @classmethod
    def api_translation_fields(cls):
        """Returns name field's translation field names"""
        return [f.name for f in cls._meta.get_fields() if f.name.startswith('name') and f.name != 'name']


class Tag(TimestampBase):
    category = models.ForeignKey(Category)
    parent_tag = models.ForeignKey('self', blank=True, null=True, default=None, related_name="children")
    name = models.CharField(max_length=100)
    create_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='tag_create_user', blank=True, null=True, default=None, on_delete=models.SET_NULL)
    update_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='tag_update_user', blank=True, null=True, default=None, on_delete=models.SET_NULL)
    image = models.ImageField(upload_to='tag/%Y/%m/%d', null=True, blank=True)
    slug = AutoSlugField(populate_from='name', max_length=100, blank=True, null=True)
    order_by = models.IntegerField(default=0)
    external_url = models.URLField(
        blank=True, null=True, default=None, max_length=500)
    description = models.TextField(blank=True, null=True, default=None)
    summary = models.CharField(blank=True, null=True, max_length=100)
    contact_email = models.CharField(blank=True, null=True, max_length=100)
    published = models.BooleanField(default=True, help_text=_(u"Used to toggle status of health domains."))

    tags = TagQuerySet.as_manager()
    objects = TagQuerySet.as_manager()
    # objects = tags  # backwards compatibility

    class Meta:
        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')
        ordering = ('name',)
        unique_together = ('name', 'category')

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return urlresolvers.reverse('orb_tags', args=[self.slug])

    def save(self, *args, **kwargs):

        if self.image and (self.image.name.startswith("http://") or self.image.name.startswith("https://")):
            remote_image_file = self.image.name
        else:
            remote_image_file = None

        # add generic geography icon if not specified
        if self.category.slug == 'geography' and not self.image:
            self.image = 'tag/geography_default.png'

        # add generic language icon if not specified
        if self.category.slug == 'language' and not self.image:
            self.image = 'tag/language_default.png'

        # add generic organization icon if not specified
        if self.category.slug == 'organisation' and not self.image:
            self.image = 'tag/organisation_default.png'

        # add generic other icon if not specified
        if self.category.slug == 'other' and not self.image:
            self.image = 'tag/other_default.png'

        super(Tag, self).save(*args, **kwargs)

        if remote_image_file:
            image_cleaner(self, url=remote_image_file)

        return self

    def image_filename(self):
        return os.path.basename(self.image.name)

    def get_property(self, name):
        props = TagProperty.objects.filter(tag=self, name=name)
        return props

    def merge(self, other):
        """
        Merges another tag into this one

        In doing so it 'merges' relations by ensuring tagged resources are maintained

        Args:
            other: the 'loser' Tag instance

        Returns:
            None

        """
        # The following is a more sensible query-based way of updating, however
        # due to a limitation in MySQL this is not possible (MySQL Error 1093):
        # >>> other.resourcetag.exclude(resource__resourcetag__tag=self).update(tag=self)

        for resource_tag in other.resourcetag.exclude(resource__resourcetag__tag=self):
            resource_tag.tag = self
            resource_tag.save()

        other.tracker.all().update(tag=self)
        other.delete()


class TagProperty(models.Model):
    tag = models.ForeignKey(Tag, related_name="properties")
    name = models.TextField(blank=False, null=False)
    value = models.TextField(blank=False, null=False)

    class Meta:
        verbose_name = _(u'Tag property')
        verbose_name_plural = _(u'Tag properties')
        ordering = ('tag', 'name', 'value')

    def __unicode__(self):
        return self.name


class TagOwner(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    tag = models.ForeignKey(Tag, related_name="owner")

    class Meta:
        unique_together = ("user", "tag")


class ResourceTag(models.Model):
    create_date = models.DateTimeField(auto_now_add=True)
    resource = models.ForeignKey(Resource)
    tag = models.ForeignKey(Tag, related_name="resourcetag")
    create_user = models.ForeignKey(User, related_name='resourcetag_create_user', blank=True, null=True, default=None, on_delete=models.SET_NULL)

    objects = ResourceTagManager()

    class Meta:
        unique_together = ("resource", "tag")
        ordering = ('id',)

    @classmethod
    def create_from_api_data(cls, resource, api_data, user=None):
        """
        Creates a new Resource object and its suite of related content based
        on a dictionary of data as returned from the ORB API

        Args:
            resource: associated resource
            api_data: serialized data from the ORB API describing a tag in detail
            user: create_user/update_user

        Returns:
            a ResourceTag instance that has been saved to the database
        """
        if not user:
            user = get_import_user()

        api_data['create_user'] = user
        api_data['update_user'] = user
        api_data.pop('id', None)
        api_data.pop('resource_uri', None)
        api_data.pop('url', None)

        category_name = api_data.pop('category').strip()
        category_fields = [f for f in Category.api_translation_fields()]
        category_name_translations = {
            field: api_data.pop(field.replace('name', 'category'), "")
            for field in category_fields
        }

        for field in api_data.keys():
            if field.startswith("category"):
                del api_data[field]

        category, created = Category.objects.get_or_create(name=category_name, defaults=category_name_translations)

        api_data['category'] = category

        tag, created = Tag.objects.get_or_create(name=api_data['name'], defaults=api_data)

        return cls.objects.create(resource=resource, tag=tag, create_user=user)


class UserProfile(TimestampBase):
    AGE_RANGE = [
        ('under_18', _(u'under 18')),
        ('18_25', _(u'18-24')),
        ('25_35', _(u'25-34')),
        ('35_50', _(u'35-50')),
        ('over_50', _(u'over 50')),
        ('none', _(u'Prefer not to say')),
    ]
    GENDER = [
        ('female', _(u'Female')),
        ('male', _(u'Male')),
        ('none', _(u'Prefer not to say')),
    ]

    user = models.OneToOneField(User)
    photo = models.ImageField(upload_to='userprofile/%Y/%m/%d', max_length=200, blank=True, null=True)
    about = models.TextField(blank=True, null=True, default=None)
    job_title = models.TextField(blank=True, null=True, default=None)
    organisation = models.ForeignKey(Tag, related_name='organisation', blank=True, null=True, default=None)
    role = models.ForeignKey(Tag, related_name='role', blank=True, null=True, default=None)
    role_other = models.TextField(blank=True, null=True, default=None)
    phone_number = models.TextField(blank=True, null=True, default=None)
    website = models.CharField(blank=True, null=True, max_length=100, default=None)
    twitter = models.CharField(blank=True, null=True, max_length=100, default=None)
    api_access = models.BooleanField(default=False, blank=False)
    gender = models.CharField(max_length=50, choices=GENDER, default='none')
    age_range = models.CharField(max_length=50, choices=AGE_RANGE, default='none')
    mailing = models.BooleanField(default=False, blank=False)
    survey = models.BooleanField(default=False, blank=False)
    reviewer_roles = models.ManyToManyField('ReviewerRole', blank=True, related_name="profiles")

    profiles = ProfilesQueryset.as_manager()
    objects = ProfilesQueryset.as_manager()
    # objects = profiles

    class Meta:
        db_table = "orb_userprofile"
        verbose_name = _(u"user profile")
        verbose_name_plural = _(u"user profiles")

    def __unicode__(self):
        return self.user.get_full_name()

    def get_twitter_url(self):
        if self.twitter is not None:
            return "https://twitter.com/" + self.twitter.replace('@', '')
        else:
            return None

    @property
    def is_reviewer(self):
        return self.reviewer_roles.exists()


class ResourceTracker(models.Model):
    VIEW = 'view'
    VIEW_API = 'view-api'
    EDIT = 'edit'
    DOWNLOAD = 'download'
    CREATE = 'create'
    TRACKER_TYPES = (
        (VIEW, _(u'View')),
        (VIEW_API, _(u'View-api')),
        (EDIT, _(u'Edit')),
        (DOWNLOAD, _(u'Download')),
        (CREATE, _(u'Create')),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, default=None, on_delete=models.SET_NULL)
    type = models.CharField(max_length=50, choices=TRACKER_TYPES, default=VIEW)
    resource = models.ForeignKey(Resource, blank=True, null=True, default=None, on_delete=models.SET_NULL)
    resource_file = models.ForeignKey(ResourceFile, blank=True, null=True, default=None, on_delete=models.SET_NULL)
    resource_url = models.ForeignKey(ResourceURL, blank=True, null=True, default=None, on_delete=models.SET_NULL)
    access_date = models.DateTimeField(auto_now_add=True)
    ip = models.GenericIPAddressField(blank=True, null=True, default=None)
    user_agent = models.TextField(blank=True, null=True, default=None)
    extra_data = models.TextField(blank=True, null=True, default=None)
    survey_intended_use = models.CharField(max_length=50, blank=True, null=True)
    survey_intended_use_other = models.TextField(blank=True, null=True, default="")
    survey_health_worker_count = models.IntegerField(blank=True, null=True)
    survey_health_worker_cadre = models.CharField(max_length=50, blank=True, null=True)

    objects = TrackerQueryset.as_manager()

    def get_location(self):
        return UserLocationVisualization.objects.filter(ip=self.ip).first()


class SearchTracker(models.Model):
    SEARCH = 'search'
    SEARCH_API = 'search-api'
    SEARCH_ADV = 'search-adv'
    SEARCH_TYPES = (
        (SEARCH, _(u'search')),
        (SEARCH_API, _(u'search-api')),
        (SEARCH_ADV, _(u'search-adv')),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True,
                             default=None, on_delete=models.SET_NULL)
    query = models.TextField(blank=True, null=True, default=None)
    no_results = models.IntegerField(blank=True, null=True, default=0)
    access_date = models.DateTimeField(auto_now_add=True)
    ip = models.GenericIPAddressField(blank=True, null=True, default=None)
    user_agent = models.TextField(blank=True, null=True, default=None)
    type = models.CharField(
        max_length=50, choices=SEARCH_TYPES, default=SEARCH)
    extra_data = models.TextField(blank=True, null=True, default=None)


class TagTracker(models.Model):
    VIEW = 'view'
    VIEW_API = 'view-api'
    VIEW_URL = 'view-url'
    TRACKER_TYPES = (
        (VIEW, _(u'View')),
        (VIEW_API, _(u'View-API')),
        (VIEW_URL, _(u'View-URL')),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True,
                             default=None, on_delete=models.SET_NULL)
    type = models.CharField(max_length=50, choices=TRACKER_TYPES, default=VIEW)
    tag = models.ForeignKey(Tag, blank=True, null=True, related_name="tracker",
                            default=None, on_delete=models.SET_NULL)
    access_date = models.DateTimeField(auto_now_add=True)
    ip = models.GenericIPAddressField(blank=True, null=True, default=None)
    user_agent = models.TextField(blank=True, null=True, default=None)
    extra_data = models.TextField(blank=True, null=True, default=None)


class ResourceRating(TimestampBase):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, null=False)
    resource = models.ForeignKey(Resource, blank=False, null=False)
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)])
    comments = models.TextField(blank=True, null=True, default=None)


class Collection(TimestampBase):
    PUBLIC = 'public'
    PRIVATE = 'private'
    VISIBILITY_TYPES = (
        (PUBLIC, _(u'Public')),
        (PRIVATE, _(u'Private')),
    )
    title = models.TextField(blank=False,
                            null=False,
                            help_text=_(u"A title for the collection"))
    description = models.TextField(blank=True,
                                   null=True,
                                   default=None,
                                   help_text=_(u"A description of the collection"))
    visibility = models.CharField(
                            max_length=50,
                            choices=VISIBILITY_TYPES,
                            default=PRIVATE)
    image = models.ImageField(
        upload_to='collection/%Y/%m/%d', null=True, blank=True)
    slug = AutoSlugField(populate_from='title', max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = _(u'Collection')
        verbose_name_plural = _(u'Collections')
        ordering = ('title',)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return urlresolvers.reverse('orb_collection', args=[self.slug])

    def image_filename(self):
        return os.path.basename(self.image.name)


class CollectionUser(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, null=False)
    collection = models.ForeignKey(Collection, blank=False, null=False)

    class Meta:
        verbose_name = _('Collection user')
        verbose_name_plural = _('Collection users')
        ordering = ('collection', 'user')


class CollectionResource(models.Model):
    resource = models.ForeignKey(Resource, blank=False, null=False)
    collection = models.ForeignKey(Collection, blank=False, null=False)
    order_by = models.IntegerField(blank=False, null=False, default=0)

    class Meta:
        verbose_name = _('Collection resource')
        verbose_name_plural = _('Collection resources')
        ordering = ('collection', 'order_by', 'resource')


class ReviewerRole(models.Model):
    """
    Models the different roles a content review might fulfill

    Set up with choices to start with.
    """
    ROLE_CHOICES = [
        ('medical', _('Medical')),
        ('technical', _('Technical')),
        ('training', _('Training')),
    ]

    name = models.CharField(max_length=100, choices=ROLE_CHOICES, unique=True, default='medical')

    roles = models.Manager()
    objects = models.Manager()
    # objects = roles

    def __unicode__(self):
        return self.get_name_display()


def get_import_user():
    try:
        return User.objects.get(username="importer")
    except User.DoesNotExist:
        user = User.objects.create(username="importer")
        user.set_unusable_password()
        user.is_active = False
        user.save()
        return user


def clean_api_data(data, *fields):
    # type: (Dict[unicode, Any], Iterable[unicode]) -> Dict[unicode, Any]
    """
    Returns API resource data with unusable translations filtered

    Args:
        data: original API data
        *fields: translated field names

    Returns:
        same API data with unsupported translations dropped

    """
    language_codes = [l[0].replace('-', '_') for l in settings.LANGUAGES]
    supported_field_translations = [
        "{}_{}".format(field, language)
        for (field, language) in itertools.product(fields, language_codes)
    ]

    def allowed_field(test_field):
        # type: (unicode) -> bool
        """Returns True if the given field name should be included"""
        if test_field in ['id', 'status']:
            return False
        if test_field in fields or test_field in supported_field_translations:
            return True
        return not any([test_field.startswith(f) for f in fields])

    return {
        key: value
        for key, value in data.items()
        if allowed_field(key)
    }
