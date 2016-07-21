import os

from django.conf import settings
from django.contrib.auth.models import User
from django.core import urlresolvers
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import Avg, Count
from django.utils.translation import ugettext_lazy as _

from tastypie.models import create_api_key
from orb.analytics.models import UserLocationVisualization
from orb.resources.managers import ResourceManager, ResourceURLManager, ApprovedManager
from orb.tags.managers import ActiveTagManager, ResourceTagManager
from .fields import AutoSlugField

models.signals.post_save.connect(create_api_key, sender=User)


class TimestampBase(models.Model):
    """Base class for adding create and update timestamp fields to models"""
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Resource(TimestampBase):
    REJECTED = 'rejected'
    PENDING_CRT = 'pending_crt'
    PENDING = PENDING_CRT
    PENDING_MRT = 'pending_mrt'
    APPROVED = 'approved'
    STATUS_TYPES = (
        (REJECTED, _('Rejected')),
        (PENDING_CRT, _('Pending CRT')),
        (PENDING_MRT, _('Pending MRT')),
        (APPROVED, _('Approved')),
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

    title = models.TextField(blank=False, null=False)
    description = models.TextField(blank=False, null=False)
    image = models.ImageField(
        upload_to='resourceimage/%Y/%m/%d', max_length=200, blank=True, null=True)
    status = models.CharField(
        max_length=50, choices=STATUS_TYPES, default=PENDING_CRT)
    create_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='resource_create_user')
    update_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='resource_update_user')
    slug = AutoSlugField(populate_from='title', max_length=100, blank=True, null=True)
    study_time_number = models.IntegerField(default=0, null=True, blank=True)
    study_time_unit = models.CharField(
        max_length=10, choices=STUDY_TIME_UNITS, blank=True, null=True)
    born_on = models.DateTimeField(blank=True, null=True, default=None)
    attribution = models.TextField(blank=True, null=True, default=None)

    resources = ResourceManager()
    objects = resources  # alias
    approved = ApprovedManager()

    class Meta:
        verbose_name = _('Resource')
        verbose_name_plural = _('Resources')
        ordering = ('title',)

    def __unicode__(self):
        return self.title

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
            c.tags = Tag.objects.filter(resourcetag__resource=self, category=c)
        return categories

    def get_category(self, category_slug):
        tags = Tag.objects.filter(
            resourcetag__resource=self, category__slug=category_slug)
        return tags

    def get_type_tags(self):
        tags = Tag.objects.filter(
            resourcetag__resource=self, category__slug='type')
        return tags

    def get_absolute_url(self):
        return urlresolvers.reverse('orb_resource', args=[self.slug])

    def tags(self):
        return Tag.objects.filter(resourcetag__resource=self)

    def get_no_hits(self):
        anon = ResourceTracker.objects.filter(resource=self, user=None).values_list('ip',
                                                                                    flat=True).distinct().count()
        identified = ResourceTracker.objects.filter(resource=self).exclude(user=None).values_list('user',
                                                                                                  flat=True).distinct().count()
        return anon + identified

    def get_geographies(self):
        tags = Tag.objects.filter(
            resourcetag__resource=self, category__slug='geography')
        return tags

    def get_devices(self):
        tags = Tag.objects.filter(
            resourcetag__resource=self, category__slug='device')
        return tags

    def get_languages(self):
        tags = Tag.objects.filter(
            resourcetag__resource=self, category__slug='language')
        return tags

    def get_license(self):
        tags = Tag.objects.filter(
            resourcetag__resource=self, category__slug='license')
        return tags

    def get_health_domains(self):
        tags = Tag.objects.filter(
            resourcetag__resource=self, category__slug='health-domain')
        return tags

    def get_rating(self):
        rating = ResourceRating.objects.filter(resource=self).aggregate(
            rating=Avg('rating'), count=Count('rating'))
        if rating['rating']:
            rating['rating'] = round(rating['rating'], 0)
        return rating


class ResourceWorkflowTracker(models.Model):
    create_date = models.DateTimeField(auto_now_add=True)
    resource = models.ForeignKey(Resource, blank=True, null=True)
    create_user = models.ForeignKey(settings.AUTH_USER_MODEL)
    status = models.CharField(
        max_length=50, choices=Resource.STATUS_TYPES, default=Resource.PENDING_CRT)
    notes = models.TextField(blank=True, null=True)
    owner_email_sent = models.BooleanField(default=False, blank=False)


class ResourceURL(TimestampBase):
    url = models.URLField(blank=False, null=False, max_length=500)
    resource = models.ForeignKey(Resource)
    title = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    order_by = models.IntegerField(default=0)
    file_size = models.IntegerField(default=0)
    image = models.ImageField(
        upload_to='resourceimage/%Y/%m/%d', max_length=200, blank=True, null=True)
    create_user = models.ForeignKey(
        User, related_name='resource_url_create_user')
    update_user = models.ForeignKey(
        User, related_name='resource_url_update_user')

    objects = ResourceURLManager()

    def __unicode__(self):
        return self.url


class ResourceFile(TimestampBase):
    file = models.FileField(upload_to='resource/%Y/%m/%d', max_length=200)
    resource = models.ForeignKey(Resource)
    title = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    order_by = models.IntegerField(default=0)
    image = models.ImageField(
        upload_to='resourceimage/%Y/%m/%d', max_length=200, blank=True, null=True)
    create_user = models.ForeignKey(
        User, related_name='resource_file_create_user')
    update_user = models.ForeignKey(
        User, related_name='resource_file_update_user')
    file_full_text = models.TextField(blank=True, null=True, default=None)

    def filename(self):
        return os.path.basename(self.file.name)

    def filesize(self):
        if os.path.isfile(settings.MEDIA_ROOT + self.file.name):
            return os.path.getsize(settings.MEDIA_ROOT + self.file.name)
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
    create_user = models.ForeignKey(
        User, related_name='resource_relationship_create_user')
    update_user = models.ForeignKey(
        User, related_name='resource_relationship_update_user')


class ResourceCriteria(models.Model):
    CATEGORIES = (
        ('qa', _('Quality Assurance')),
        ('value', _('Value for Frontline Health Workers (FLHW)')),
        ('video', _('Video resources')),
        ('animation', _('Animation resources')),
        ('audio', _('Audio resources')),
        ('text', _('Text based resources')),
    )
    description = models.TextField(blank=False, null=False)
    order_by = models.IntegerField(default=0)
    category = models.CharField(max_length=50, choices=CATEGORIES)
    category_order_by = models.IntegerField(default=0)


class Category(models.Model):
    name = models.CharField(blank=False, null=False, max_length=100)
    top_level = models.BooleanField(null=False, default=False)
    slug = AutoSlugField(populate_from='name', max_length=100, blank=True, null=True)
    order_by = models.IntegerField(default=0)

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
        ordering = ('name',)

    def __unicode__(self):
        return self.name


class Tag(TimestampBase):
    category = models.ForeignKey(Category)
    parent_tag = models.ForeignKey('self', blank=True, null=True, default=None)
    name = models.CharField(blank=False, null=False, max_length=100)
    create_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='tag_create_user')
    update_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='tag_update_user')
    image = models.ImageField(upload_to='tag/%Y/%m/%d', null=True, blank=True)
    slug = AutoSlugField(populate_from='name', max_length=100, blank=True, null=True)
    order_by = models.IntegerField(default=0)
    external_url = models.URLField(
        blank=True, null=True, default=None, max_length=500)
    description = models.TextField(blank=True, null=True, default=None)
    summary = models.CharField(blank=True, null=True, max_length=100)
    contact_email = models.CharField(blank=True, null=True, max_length=100)

    objects = models.Manager()
    active = ActiveTagManager()

    class Meta:
        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')
        ordering = ('name',)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return urlresolvers.reverse('orb_tags', args=[self.slug])

    def save(self, *args, **kwargs):
        # add generic geography icon if not specified
        if self.category.slug == 'geography' and not self.image:
            self.image = 'tag/geography_default.png'

        # add generic language icon if not specified
        if self.category.slug == 'language' and not self.image:
            self.image = 'tag/language_default.png'

        super(Tag, self).save(*args, **kwargs)

    def image_filename(self):
        return os.path.basename(self.image.name)

    def get_property(self, name):
        props = TagProperty.objects.filter(tag=self, name=name)
        return props


class TagProperty(models.Model):
    tag = models.ForeignKey(Tag)
    name = models.TextField(blank=False, null=False)
    value = models.TextField(blank=False, null=False)

    class Meta:
        verbose_name = _('Tag property')
        verbose_name_plural = _('Tag properties')
        ordering = ('tag', 'name', 'value')

    def __unicode__(self):
        return self.name


class TagOwner(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    tag = models.ForeignKey(Tag)

    class Meta:
        unique_together = ("user", "tag")


class ResourceTag(models.Model):
    create_date = models.DateTimeField(auto_now_add=True)
    resource = models.ForeignKey(Resource)
    tag = models.ForeignKey(Tag)
    create_user = models.ForeignKey(
        User, related_name='resourcetag_create_user')

    objects = ResourceTagManager()

    class Meta:
        unique_together = ("resource", "tag")


class UserProfile(TimestampBase):
    AGE_RANGE = (
        ('under_18', _('under 18')),
        ('18_25', _('18-24')),
        ('25_35', _('25-34')),
        ('35_50', _('35-50')),
        ('over_50', _('over 50')),
        ('none', _('Prefer not to say')),
    )
    GENDER = (
        ('female', _('Female')),
        ('male', _('Male')),
        ('none', _('Prefer not to say')),
    )

    user = models.OneToOneField(User)
    photo = models.ImageField(
        upload_to='userprofile/%Y/%m/%d', max_length=200, blank=True, null=True)
    about = models.TextField(blank=True, null=True, default=None)
    job_title = models.TextField(blank=True, null=True, default=None)
    organisation = models.ForeignKey(
        Tag, related_name='organisation', blank=True, null=True, default=None)
    role = models.ForeignKey(Tag, related_name='role',
                             blank=True, null=True, default=None)
    role_other = models.TextField(blank=True, null=True, default=None)
    phone_number = models.TextField(blank=True, null=True, default=None)
    website = models.CharField(
        blank=True, null=True, max_length=100, default=None)
    twitter = models.CharField(
        blank=True, null=True, max_length=100, default=None)
    api_access = models.BooleanField(default=False, blank=False)
    gender = models.CharField(max_length=50, choices=GENDER, default='none')
    age_range = models.CharField(
        max_length=50, choices=AGE_RANGE, default='none')
    mailing = models.BooleanField(default=False, blank=False)
    crt_member = models.BooleanField(default=False, blank=False)
    mep_member = models.BooleanField(default=False, blank=False)
    reviewer_role = models.ForeignKey('ReviewerRole', blank=True, null=True)

    class Meta:
        db_table = "orb_userprofile"

    def get_twitter_url(self):
        if self.twitter is not None:
            return "https://twitter.com/" + self.twitter.replace('@', '')
        else:
            return None

    @property
    def is_reviewer(self):
        return self.crt_member or self.mep_member


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
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True,
                             default=None, on_delete=models.SET_NULL)
    type = models.CharField(max_length=50, choices=TRACKER_TYPES, default=VIEW)
    resource = models.ForeignKey(
        Resource, blank=True, null=True, default=None, on_delete=models.SET_NULL)
    resource_file = models.ForeignKey(
        ResourceFile, blank=True, null=True, default=None, on_delete=models.SET_NULL)
    resource_url = models.ForeignKey(
        ResourceURL, blank=True, null=True, default=None, on_delete=models.SET_NULL)
    access_date = models.DateTimeField(auto_now_add=True)
    ip = models.GenericIPAddressField(blank=True, null=True, default=None)
    user_agent = models.TextField(blank=True, null=True, default=None)
    extra_data = models.TextField(blank=True, null=True, default=None)

    def get_location(self):
        try:
            return UserLocationVisualization.objects.filter(ip=self.ip).first()
        except UserLocationVisualization.DoesNotExist:
            return None


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
    tag = models.ForeignKey(Tag, blank=True, null=True,
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
    title = models.TextField(blank=False, null=False)
    description = models.TextField(blank=True, null=True, default=None)
    visibility = models.CharField(
        max_length=50, choices=VISIBILITY_TYPES, default=PRIVATE)
    image = models.ImageField(
        upload_to='collection/%Y/%m/%d', null=True, blank=True)
    slug = AutoSlugField(populate_from='title', max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = _('Collection')
        verbose_name_plural = _('Collections')
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
        ('other', _('Other')),
    ]

    name = models.CharField(max_length=100, choices=ROLE_CHOICES, unique=True, default='medical')
