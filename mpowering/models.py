

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
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
