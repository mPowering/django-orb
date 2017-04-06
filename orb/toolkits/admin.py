from django.contrib import admin

from orb.toolkits.models import Toolkit


@admin.register(Toolkit)
class ToolkitAdmin(admin.ModelAdmin):
    list_display = ('title', 'order_by')

