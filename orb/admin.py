from django import forms
from django.conf.urls import url
from django.contrib import admin
from django.contrib import messages
from django.db.models import Value as V, F
from django.db.models.functions import Concat
from django.shortcuts import get_object_or_404, render, redirect
from django.utils.translation import ugettext_lazy as _

from orb.actions import merge_selected_tags
from orb.models import Category, Tag, Resource, ResourceURL, TagProperty
from orb.models import Collection, CollectionUser, CollectionResource, ReviewerRole
from orb.models import ResourceFile, ResourceTag, UserProfile, ResourceCriteria
from orb.models import ResourceTracker, SearchTracker, TagOwner, ResourceWorkflowTracker, ResourceRating


class TagMergeForm(forms.Form):
    tag = forms.ModelChoiceField(queryset=Tag.tags.all(), label=_('Winner'))

    def __init__(self, other=None, *args, **kwargs):
        super(TagMergeForm, self).__init__(*args, **kwargs)
        if other:
            self.fields['tag'].queryset = Tag.tags.exclude(pk=other.pk)


class ReviewerFilter(admin.SimpleListFilter):
    """
    List filter for UserProfiles, to filter by reviewer status
    """
    title = _('is reviewer')
    parameter_name = 'reviewer'

    def lookups(self, request, model_admin):
        return (
            ('1', _('Yes')),
            ('0', _('No')),
        )

    def queryset(self, request, queryset):
        if self.value() == '1':
            return queryset.reviewers()
        if self.value() == '0':
            return queryset.nonreviewers()


class ResourceCriteriaInline(admin.TabularInline):
    """Inline class for showing related ResourceCriteria"""
    model = ResourceCriteria
    extra = 0


@admin.register(ReviewerRole)
class ReviewerRoleAdmin(admin.ModelAdmin):
    inlines = [ResourceCriteriaInline]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'top_level', 'slug', 'order_by')


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'create_user', 'create_date', 'slug')
    search_fields = ['title', 'description']
    raw_id_fields = ('create_user', 'update_user')
    list_filter = ('status',)


@admin.register(ResourceCriteria)
class ResourceCriteriaAdmin(admin.ModelAdmin):
    list_display = ('description', 'get_role_display', 'order_by', )
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
                    'slug', 'published', 'parent_tag', 'order_by', 'image')
    search_fields = ['name', 'description']
    raw_id_fields = ('create_user', 'update_user', 'category', 'parent_tag')
    list_filter = ['category']
    actions = [merge_selected_tags]

    def get_urls(self):
        urls = super(TagAdmin, self).get_urls()
        my_urls = [
            url(r'^(?P<object_id>\d+)/merge/$', self.admin_site.admin_view(self.merge_tags), name="merge_tags"),
        ]
        return my_urls + urls

    def merge_tags(self, request, object_id):
        tag = get_object_or_404(Tag, pk=object_id)

        form = TagMergeForm(tag)

        if request.method == 'POST':
            form = TagMergeForm(tag, data=request.POST)
            if form.is_valid():
                winner = form.cleaned_data['tag']
                winner.merge(tag)
                messages.success(request, u"The tag '{}' was merged into '{}'".format(tag, winner))
                return redirect('admin:orb_tag_changelist')

        context = dict(
            self.admin_site.each_context(request),
            app_label='orb',
            tag=tag,
            form=form,
        )
        return render(request, "admin/orb/tag/merge_tag_form.html", context)


@admin.register(TagProperty)
class TagPropertyAdmin(admin.ModelAdmin):
    list_display = ('tag', 'name', 'value')
    search_fields = ['name', 'value']
    raw_id_fields = ('tag',)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name')
    list_display = ('user_name', 'api_access', 'about', 'job_title', 'organisation')
    list_filter = (
        ReviewerFilter,
        'reviewer_roles',
    )

    def get_queryset(self, request):
        return super(UserProfileAdmin, self).get_queryset(request).annotate(
            full_user_name=Concat(
                F('user__first_name'),
                V(' '),
                F('user__last_name'),
            )
        )

    def user_name(self, obj):
        return obj.user.get_full_name()
    user_name.admin_order_field = 'full_user_name'


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
