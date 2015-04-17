from django.contrib import admin

from mpowering.analytics.models import UserLocationVisualization

# Register your models here.

    
class UserLocationVisualizationAdmin(admin.ModelAdmin):
    list_display = ('ip','hits','country_code','region')
                 
admin.site.register(UserLocationVisualization,UserLocationVisualizationAdmin)
