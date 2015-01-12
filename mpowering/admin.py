from django.contrib import admin

from mpowering.models import Category, Tag, Resource
# Register your models here.

    
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name','top_level','slug','order_by')

class TagAdmin(admin.ModelAdmin):
    list_display = ('name','category', 'slug','order_by')

admin.site.register(Category,CategoryAdmin)
admin.site.register(Tag, TagAdmin) 
admin.site.register(Resource)  
