from django.contrib import admin

from .models import Peer, PeerQueryLog


@admin.register(Peer)
class PeerAdmin(admin.ModelAdmin):
    pass


@admin.register(PeerQueryLog)
class PeerQueryLogAdmin(admin.ModelAdmin):
    pass
