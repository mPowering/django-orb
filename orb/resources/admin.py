from django.contrib import admin

from .models import ContentReview


@admin.register(ContentReview)
class ContentReviewAdmin(admin.ModelAdmin):
    raw_id_fields = ['resource', 'reviewer']
