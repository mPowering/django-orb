from django.contrib import admin

from orb.courses import forms
from orb.courses import models


@admin.register(models.Course)
class CourseAdmin(admin.ModelAdmin):
    form = forms.CourseAdminForm
    list_display = ['title', 'status', 'create_user']
