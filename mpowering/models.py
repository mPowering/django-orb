import os

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from tastypie.models import create_api_key
from utils.unique_slugify import unique_slugify

models.signals.post_save.connect(create_api_key, sender=User)


# Create your models here.

# Organisation
class Organisation (models.Model):
    name = models.TextField(blank=False, null=False)
    location = models.TextField(blank=True, null=True, default=None)
    url = models.URLField(blank=True, null=True, default=None)
    create_date = models.DateTimeField(default=timezone.now)
    create_user = models.ForeignKey(User, related_name='organisation_create_user')
    update_date = models.DateTimeField(default=timezone.now) 
    update_user = models.ForeignKey(User, related_name='organisation_update_user')
     
    def __unicode__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.update_date = timezone.now()
        super(Organisation, self).save(*args, **kwargs)
        
# UserProfile
class UserProfile (models.Model):
    user = models.OneToOneField(User)
    about = models.TextField(blank=True, null=True, default=None)
    job_title = models.TextField(blank=True, null=True, default=None)
    organisation = models.ForeignKey(Organisation)
    phone_number = models.TextField(blank=True, null=True, default=None)
    create_date = models.DateTimeField(default=timezone.now)
    update_date = models.DateTimeField(default=timezone.now)
    
    def save(self, *args, **kwargs):
        self.update_date = timezone.now()
        super(UserProfile, self).save(*args, **kwargs)
        
# Resource
class Resource (models.Model):
    REJECTED = 'rejected'
    PENDING = 'pending'
    APPROVED = 'approved'
    STATUS_TYPES = (
        (REJECTED, _('Rejected')),
        (PENDING, _('Pending')),
        (APPROVED, _('Approved')),
    )
    
    title = models.TextField(blank=False, null=False)
    description = models.TextField(blank=False, null=False) 
    image = models.ImageField(upload_to='resourceimage/%Y/%m/%d', max_length=200, blank=True, null=True)
    status = models.CharField(max_length=50,choices=STATUS_TYPES)
    create_date = models.DateTimeField(default=timezone.now)
    create_user = models.ForeignKey(User, related_name='resource_create_user')
    update_date = models.DateTimeField(default=timezone.now) 
    update_user = models.ForeignKey(User, related_name='resource_update_user')
    slug = models.CharField(blank=True, null=True, max_length=100)
    
    class Meta:
        verbose_name = _('Resource')
        verbose_name_plural = _('Resources')
        
    def __unicode__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        unique_slugify(self, self.title)
        self.update_date = timezone.now()
        super(Resource, self).save(*args, **kwargs)
    
    def get_organisations(self):
        return Organisation.objects.filter(resourceorganisation__resource=self)
    
    def get_files(self):
        return ResourceFile.objects.filter(resource=self)
    
    def get_urls(self):
        return ResourceURL.objects.filter(resource=self)
    
    def get_categories(self):
        categories = Category.objects.filter(tag__resourcetag__resource=self).distinct().order_by('order_by')
        for c in categories:
            c.tags = Tag.objects.filter(resourcetag__resource=self, category=c)
        return categories
    
    def get_category(self, category_slug):
        tags = Tag.objects.filter(resourcetag__resource=self, category__slug=category_slug)
        return tags
    
    def get_type_tags(self):
        tags = Tag.objects.filter(resourcetag__resource=self, category__slug='type')
        return tags
    
# ResourceURL
class ResourceURL (models.Model):
    url = models.URLField(blank=False, null=False, max_length=500)
    resource = models.ForeignKey(Resource)
    description = models.TextField(blank=True, null=True) 
    create_date = models.DateTimeField(default=timezone.now)
    create_user = models.ForeignKey(User, related_name='resource_url_create_user')
    update_date = models.DateTimeField(default=timezone.now) 
    update_user = models.ForeignKey(User, related_name='resource_url_update_user')

    def __unicode__(self):
        if self.description is None:
            return self.url
        else:
            return self.description
        
    def save(self, *args, **kwargs):
        self.update_date = timezone.now()
        super(ResourceURL, self).save(*args, **kwargs)
        
# ResourceFile
class ResourceFile (models.Model):
    file = models.FileField(upload_to='resource/%Y/%m/%d', max_length=200)
    resource = models.ForeignKey(Resource)
    description = models.TextField(blank=True, null=True) 
    create_date = models.DateTimeField(default=timezone.now)
    create_user = models.ForeignKey(User, related_name='resource_file_create_user')
    update_date = models.DateTimeField(default=timezone.now) 
    update_user = models.ForeignKey(User, related_name='resource_file_update_user')

    def save(self, *args, **kwargs):
        self.update_date = timezone.now()
        super(ResourceFile, self).save(*args, **kwargs)
    
    def filename(self):
        return os.path.basename(self.file.name)
        
# ResourceRelationship
class ResourceRelationship (models.Model):
    RELATIONSHIP_TYPES = (
        ('is_translation_of', _('is translation of')),
        ('is_derivative_of', _('is derivative of')),
        ('is_contained_in', _('is contained in')),
    )
    
    resource = models.ForeignKey(Resource, related_name='resource')
    resource_related = models.ForeignKey(Resource, related_name='resource_related')
    relationship_type = models.CharField(max_length=50,choices=RELATIONSHIP_TYPES)
    description = models.TextField(blank=False, null=False) 
    create_date = models.DateTimeField(default=timezone.now)
    create_user = models.ForeignKey(User, related_name='resource_relationship_create_user')
    update_date = models.DateTimeField(default=timezone.now) 
    update_user = models.ForeignKey(User, related_name='resource_relationship_update_user')
    
    def save(self, *args, **kwargs):
        self.update_date = timezone.now()
        super(ResourceRelationship, self).save(*args, **kwargs)
        
# Category
class Category (models.Model):
    name = models.CharField(blank=False, null=False, max_length=100) 
    top_level = models.BooleanField(null=False,default=False)
    slug = models.CharField(blank=True, null=True, max_length=100) 
    order_by = models.IntegerField(default=0)
    
    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
        
    def __unicode__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        # If there is not already a slug in place...
        if not self.slug:
            # Import django's builtin slug function
            from django.template.defaultfilters import slugify
            # Call this slug function on the field you want the slug to be made of
            self.slug = slugify(self.name)
        # Call the rest of the old save() method
        super(Category, self).save(*args, **kwargs)
        
            
# Tag
class Tag (models.Model):
    category = models.ForeignKey(Category)
    name = models.CharField(blank=False, null=False, max_length=100)
    create_date = models.DateTimeField(default=timezone.now)
    create_user = models.ForeignKey(User, related_name='tag_create_user')
    update_date = models.DateTimeField(default=timezone.now) 
    update_user = models.ForeignKey(User, related_name='tag_update_user')
    image = models.ImageField(upload_to='tag', null=True, blank=True)
    slug = models.CharField(blank=True, null=True, max_length=100)
    order_by = models.IntegerField(default=0)
    
    class Meta:
        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')
        
    def __unicode__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        unique_slugify(self, self.name)
        self.update_date = timezone.now()
        super(Tag, self).save(*args, **kwargs)
        
# ResourceTag
class ResourceTag (models.Model):
    resource = models.ForeignKey(Resource)
    tag = models.ForeignKey(Tag)
    create_date = models.DateTimeField(default=timezone.now)
    create_user = models.ForeignKey(User, related_name='resourcetag_create_user')   

# ResourceOrganisation
class ResourceOrganisation (models.Model):
    resource = models.ForeignKey(Resource)
    organisation = models.ForeignKey(Organisation)
    create_date = models.DateTimeField(default=timezone.now)
    create_user = models.ForeignKey(User)  
    
class Tracker(models.Model):
    VIEW = 'view'
    EDIT = 'edit'
    DOWNLOAD = 'download'
    CREATE = 'create'
    TRACKER_TYPES = (
        (VIEW, _(u'View')),
        (EDIT, _(u'Edit')),
        (DOWNLOAD, _(u'Download')),
        (CREATE, _(u'Create')),
    )
    user = models.ForeignKey(User, blank=True, null=True, default=None)
    type = models.CharField(max_length=50,choices=TRACKER_TYPES)
    resource = models.ForeignKey(Resource, blank=True, null=True, default=None)
    resource_file = models.ForeignKey(ResourceFile, blank=True, null=True, default=None)
    resource_url = models.ForeignKey(ResourceURL, blank=True, null=True, default=None)
    access_date = models.DateTimeField(default=timezone.now)
    ip = models.IPAddressField(blank=True, null=True, default=None)
    user_agent = models.TextField(blank=True, null=True, default=None)
    extra_data = models.TextField(blank=True, null=True, default=None)
    
