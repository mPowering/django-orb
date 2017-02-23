from django.contrib import admin

from .models import Peer, PeerQueryLog


@admin.register(Peer)
class PeerAdmin(admin.ModelAdmin):
    pass


@admin.register(PeerQueryLog)
class PeerQueryLogAdmin(admin.ModelAdmin):
    list_display = ('peer', 'created', 'new_resources', 'skipped_local_resources', 'updated_resources')
    readonly_fields = ('peer', 'created', 'finished', 'filtered_date', 'new_resources',
                       'skipped_local_resources', 'updated_resources', 'unchanged_resources')
    list_filter = ('peer',)

    def has_delete_permission(self, request, obj=None):
        return False
