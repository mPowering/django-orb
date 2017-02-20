from django.contrib import admin

from .models import Peer, PeerQueryLog


@admin.register(Peer)
class PeerAdmin(admin.ModelAdmin):
    pass


@admin.register(PeerQueryLog)
class PeerQueryLogAdmin(admin.ModelAdmin):
    readonly_fields = ('peer',)
    list_display = ('peer', 'created')
    list_filter = ('peer',)

    def has_delete_permission(self, request, obj=None):
        return False
