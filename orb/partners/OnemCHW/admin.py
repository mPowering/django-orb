from django.contrib import admin

from orb.partners.OnemCHW.models import CountryData
    
    
class CountryDataAdmin(admin.ModelAdmin):
    list_display = ('country_name', 'slug', 'country_code')
                 
admin.site.register(CountryData,CountryDataAdmin)
