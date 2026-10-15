from django.contrib.admin import ModelAdmin, register
from apps.reviews.models import Review


@register(Review)
class ReviewAdmin(ModelAdmin):
    list_display = ('review_id', 'user', 'order', 'review_score', 'created_at')
    list_filter = ('review_score', 'created_at')
    search_fields = ('review_id', 'user__email', 'comment')
    readonly_fields = ('review_id', 'created_at', 'updated_at', 'deleted_at')