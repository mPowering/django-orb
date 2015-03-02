from django.contrib import admin

from mpowering.models import Category, Tag, Resource, ResourceURL
from mpowering.models import ResourceFile, ResourceTag, UserProfile, ResourceTracker, SearchTracker
# Register your models here.

    
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name','top_level','slug','order_by')

class ResourceAdmin(admin.ModelAdmin):
    list_display = ('title','status', 'create_user', 'create_date', 'slug')
    
class ResourceURLAdmin(admin.ModelAdmin):
    list_display = ('resource', 'url', 'description')

class ResourceFileAdmin(admin.ModelAdmin):
    list_display = ('resource', 'file', 'description')
  
class ResourceTagAdmin(admin.ModelAdmin):
    list_display = ('resource', 'tag')

class ResourceTrackerAdmin(admin.ModelAdmin):
    list_display = ('resource', 'user', 'access_date', 'ip', 'type')
  
class SearchTrackerAdmin(admin.ModelAdmin):
    list_display = ('query', 'user', 'access_date', 'no_results', 'ip', 'type')
        
class TagAdmin(admin.ModelAdmin):
    list_display = ('name','category', 'slug', 'order_by')

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'about', 'job_title', 'organisation')
                 
admin.site.register(Category,CategoryAdmin)
admin.site.register(Tag, TagAdmin) 
admin.site.register(Resource, ResourceAdmin) 
admin.site.register(ResourceURL, ResourceURLAdmin)
admin.site.register(ResourceFile, ResourceFileAdmin)
admin.site.register(ResourceTag, ResourceTagAdmin)
admin.site.register(ResourceTracker, ResourceTrackerAdmin)
admin.site.register(SearchTracker, SearchTrackerAdmin)
admin.site.register(UserProfile, UserProfileAdmin)