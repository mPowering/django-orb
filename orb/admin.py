from django.contrib import admin

from orb.models import Category, Tag, Resource, ResourceURL, TagProperty
from orb.models import ResourceFile, ResourceTag, UserProfile, ResourceCriteria
from orb.models import ResourceTracker, SearchTracker, TagOwner, ResourceWorkflowTracker, ResourceRating
from orb.models import Collection, CollectionUser, CollectionResource, ReviewerRole


@admin.register(ReviewerRole)
class ReviewerRoleAdmin(admin.ModelAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'top_level', 'slug', 'order_by')


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'create_user', 'create_date', 'slug')
    search_fields = ['title', 'description']
    raw_id_fields = ('create_user', 'update_user')


@admin.register(ResourceCriteria)
class ResourceCriteriaAdmin(admin.ModelAdmin):
    list_display = ('description', 'category',
                    'category_order_by', 'order_by', )
    search_fields = ['description']


@admin.register(ResourceURL)
class ResourceURLAdmin(admin.ModelAdmin):
    list_display = ('resource', 'url', 'title', 'description')
    search_fields = ['title', 'description', 'url']
    raw_id_fields = ('create_user', 'update_user')


@admin.register(ResourceFile)
class ResourceFileAdmin(admin.ModelAdmin):
    list_display = ('resource', 'file', 'title', 'description')
    search_fields = ['title', 'description']
    raw_id_fields = ('create_user', 'update_user')


@admin.register(ResourceTag)
class ResourceTagAdmin(admin.ModelAdmin):
    list_display = ('resource', 'tag')
    raw_id_fields = ('resource', 'tag', 'create_user')


@admin.register(ResourceRating)
class ResourceRatingAdmin(admin.ModelAdmin):
    list_display = ('resource', 'rating', 'user', 'comments')
    raw_id_fields = ('resource', 'user')


@admin.register(ResourceTracker)
class ResourceTrackerAdmin(admin.ModelAdmin):
    list_display = ('resource', 'user', 'access_date', 'ip', 'type')
    raw_id_fields = ('resource', 'user', 'resource_file', 'resource_url')


@admin.register(ResourceWorkflowTracker)
class ResourceWorkflowTrackerAdmin(admin.ModelAdmin):
    list_display = ('resource', 'create_user', 'create_date',
                    'status', 'notes', 'owner_email_sent')
    search_fields = ['notes']
    raw_id_fields = ('resource', 'create_user')


@admin.register(SearchTracker)
class SearchTrackerAdmin(admin.ModelAdmin):
    list_display = ('query', 'user', 'access_date', 'no_results', 'ip', 'type')
    raw_id_fields = ('user',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'external_url',
                    'slug', 'parent_tag', 'order_by', 'image')
    search_fields = ['name', 'description']
    raw_id_fields = ('create_user', 'update_user', 'category', 'parent_tag')


@admin.register(TagProperty)
class TagPropertyAdmin(admin.ModelAdmin):
    list_display = ('tag', 'name', 'value')
    search_fields = ['name', 'value']
    raw_id_fields = ('tag',)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'api_access', 'about', 'job_title', 'organisation')


@admin.register(TagOwner)
class TagOwnerAdmin(admin.ModelAdmin):
    list_display = ('user', 'tag')
    raw_id_fields = ('user', 'tag')


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'visibility')


@admin.register(CollectionResource)
class CollectionResourceAdmin(admin.ModelAdmin):
    list_display = ('collection', 'resource', 'order_by')
    raw_id_fields = ('resource',)


@admin.register(CollectionUser)
class CollectionUserAdmin(admin.ModelAdmin):
    list_display = ('collection', 'user')
