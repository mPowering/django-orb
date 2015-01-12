

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from tastypie.models import create_api_key

models.signals.post_save.connect(create_api_key, sender=User)


# Create your models here.

# Organisation
class Organisation (models.Model):
    name = models.TextField(blank=False, null=False)
    location = models.TextField(blank=True, null=True, default=None)
    create_date = models.DateTimeField(default=timezone.now)
    create_user = models.ForeignKey(User, related_name='organisation_create_user')
    update_date = models.DateTimeField(default=timezone.now) 
    update_user = models.ForeignKey(User, related_name='organisation_update_user')
    
# UserProfile
class UserProfile (models.Model):
    user = models.OneToOneField(User)
    about = models.TextField(blank=True, null=True, default=None)
    job_title = models.TextField(blank=True, null=True, default=None)
    organisation = models.OneToOneField(Organisation)
    phone_number = models.TextField(blank=True, null=True, default=None)
    create_date = models.DateTimeField(default=timezone.now)
    update_date = models.DateTimeField(default=timezone.now)
    
# Resource
class Resource (models.Model):
    title = models.TextField(blank=False, null=False)
    description = models.TextField(blank=False, null=False) 
    create_date = models.DateTimeField(default=timezone.now)
    create_user = models.ForeignKey(User, related_name='resource_create_user')
    update_date = models.DateTimeField(default=timezone.now) 
    update_user = models.ForeignKey(User, related_name='resource_update_user')
    
# ResourceURL
class ResourceURL (models.Model):
    url = models.TextField(blank=False, null=False)
    resource = models.ForeignKey(Resource)
    description = models.TextField(blank=False, null=False) 
    create_date = models.DateTimeField(default=timezone.now)
    create_user = models.ForeignKey(User, related_name='resource_url_create_user')
    update_date = models.DateTimeField(default=timezone.now) 
    update_user = models.ForeignKey(User, related_name='resource_url_update_user')

# ResourceFile
class ResourceFile (models.Model):
    file = models.FileField(upload_to='mpowering/%Y/%m/%d', max_length=200)
    resource = models.ForeignKey(Resource)
    description = models.TextField(blank=False, null=False) 
    create_date = models.DateTimeField(default=timezone.now)
    create_user = models.ForeignKey(User, related_name='resource_file_create_user')
    update_date = models.DateTimeField(default=timezone.now) 
    update_user = models.ForeignKey(User, related_name='resource_file_update_user')
    
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
    
# Category
class Category (models.Model):
    name = models.TextField(blank=False, null=False) 
    slug = models.TextField(blank=False, null=False)
    top_level = models.BooleanField(null=False,default=False)
    
# Tag
class Tag (models.Model):
    category = models.ForeignKey(Category)
    name = models.TextField(blank=False, null=False)
    create_date = models.DateTimeField(default=timezone.now)
    create_user = models.ForeignKey(User, related_name='tag_create_user')
    update_date = models.DateTimeField(default=timezone.now) 
    update_user = models.ForeignKey(User, related_name='tag_update_user')
    
# ResourceTag
class ResourceTag (models.Model):
    resource = models.ForeignKey(Resource)
    tag = models.ForeignKey(Tag)
    create_date = models.DateTimeField(default=timezone.now)
    create_user = models.ForeignKey(User, related_name='resourcetag_create_user')   
    
