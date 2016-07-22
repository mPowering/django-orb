from django.contrib import admin

from orb.models import Category, Tag, Resource, ResourceURL, TagProperty
from orb.models import ResourceFile, ResourceTag, UserProfile, ResourceCriteria
from orb.models import ResourceTracker, SearchTracker, TagOwner, ResourceWorkflowTracker, ResourceRating
from orb.models import Collection, CollectionUser, CollectionResource, ReviewerRole


@admin.register(ReviewerRole)
class ReviewerRoleAdmin(admin.ModelAdmin):
    pass


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'top_level', 'slug', 'order_by')


class ResourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'create_user', 'create_date', 'slug')
    search_fields = ['title', 'description']


class ResourceCriteriaAdmin(admin.ModelAdmin):
    list_display = ('description', 'category',
                    'category_order_by', 'order_by', )
    search_fields = ['description']


class ResourceURLAdmin(admin.ModelAdmin):
    list_display = ('resource', 'url', 'title', 'description')
    search_fields = ['title', 'description', 'url']


class ResourceFileAdmin(admin.ModelAdmin):
    list_display = ('resource', 'file', 'title', 'description')
    search_fields = ['title', 'description']


class ResourceTagAdmin(admin.ModelAdmin):
    list_display = ('resource', 'tag')


class ResourceRatingAdmin(admin.ModelAdmin):
    list_display = ('resource', 'rating', 'user', 'comments')


class ResourceTrackerAdmin(admin.ModelAdmin):
    list_display = ('resource', 'user', 'access_date', 'ip', 'type')


class ResourceWorkflowTrackerAdmin(admin.ModelAdmin):
    list_display = ('resource', 'create_user', 'create_date',
                    'status', 'notes', 'owner_email_sent')
    search_fields = ['notes']


class SearchTrackerAdmin(admin.ModelAdmin):
    list_display = ('query', 'user', 'access_date', 'no_results', 'ip', 'type')


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'external_url',
                    'slug', 'parent_tag', 'order_by', 'image')
    search_fields = ['name', 'description']


class TagPropertyAdmin(admin.ModelAdmin):
    list_display = ('tag', 'name', 'value')
    search_fields = ['name', 'value']


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'api_access', 'about', 'job_title', 'organisation')


class TagOwnerAdmin(admin.ModelAdmin):
    list_display = ('user', 'tag')


class CollectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'visibility')


class CollectionResourceAdmin(admin.ModelAdmin):
    list_display = ('collection', 'resource', 'order_by')


@admin.register(CollectionUser)
class CollectionUserAdmin(admin.ModelAdmin):
    list_display = ('collection', 'user')

admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(TagProperty, TagPropertyAdmin)
admin.site.register(TagOwner, TagOwnerAdmin)
admin.site.register(Resource, ResourceAdmin)
admin.site.register(ResourceCriteria, ResourceCriteriaAdmin)
admin.site.register(ResourceURL, ResourceURLAdmin)
admin.site.register(ResourceFile, ResourceFileAdmin)
admin.site.register(ResourceTag, ResourceTagAdmin)
admin.site.register(ResourceTracker, ResourceTrackerAdmin)
admin.site.register(ResourceWorkflowTracker, ResourceWorkflowTrackerAdmin)
admin.site.register(SearchTracker, SearchTrackerAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(ResourceRating, ResourceRatingAdmin)
admin.site.register(Collection, CollectionAdmin)
admin.site.register(CollectionResource, CollectionResourceAdmin)
