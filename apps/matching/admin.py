from django.contrib.admin import ModelAdmin, register
from django.core.handlers.wsgi import WSGIRequest
from django.utils.safestring import mark_safe

from apps.matching.forms import CarSearchQueryAdminForm
from apps.matching.models import CarSearchQuery


@register(CarSearchQuery)
class CarSearchQueryAdmin(ModelAdmin):
    """CarSearchQuery admin panel configuration class."""

    form = CarSearchQueryAdminForm

    list_display = (
        "search_id",
        "user",
        "model",
        "year",
        "min_price",
        "max_price",
        "results_count",
        "is_deleted",
        "created_at",
    )
    list_display_links = (
        "search_id",
    )
    list_filter = (
        "year",
        "created_at",
    )
    search_fields = (
        "search_id",
        "model",
        "user__email",
        "user__full_name",
    )
    readonly_fields = (
        "search_id",
        "created_at",
        "updated_at",
        "deleted_at",
    )
    fieldsets = (
        (
            "Search criteria",
            {
                "fields": (
                    "search_id",
                    "user",
                    "model",
                    "year",
                    ("min_price", "max_price"),
                    "results_count",
                ),
            },
        ),
        (
            "Date and time information",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                    "deleted_at",
                ),
            },
        ),
    )
    list_per_page = 50

    def is_deleted(self, instance: CarSearchQuery | None = None) -> str:
        """Return HTML badge indicating soft-deletion status."""
        if isinstance(instance, CarSearchQuery):
            if not instance.deleted_at:
                return mark_safe('<span style="color: green; font-weight: bold;">Not deleted</span>')
            return mark_safe('<span style="color: red; font-weight: bold;">Deleted</span>')
        return mark_safe('<span style="color: gray; font-weight: bold;">Unknown</span>')

    is_deleted.short_description = "Status"

    def has_delete_permission(
        self,
        request: WSGIRequest,
        obj: CarSearchQuery | None = None,
    ) -> bool:
        """Prevent deleting objects that have already been soft-deleted."""
        if obj and obj.deleted_at is not None:
            return False
        return super().has_delete_permission(request, obj)