from django.contrib import admin

from .models import ContentReview, ReviewLogEntry


@admin.register(ContentReview)
class ContentReviewAdmin(admin.ModelAdmin):
    raw_id_fields = ['resource', 'reviewer']


@admin.register(ReviewLogEntry)
class ReviewLogAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'create_date')
