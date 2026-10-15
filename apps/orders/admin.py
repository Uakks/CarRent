from django.contrib import admin 
from .models import Order 

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Настройка отображения заказов в Django Admin."""

    list_display = (
        "order_id",
        "user",
        "car",
        "start_datetime",
        "end_datetime",
        "total_price",
    )
    list_filter = ("start_datetime", "end_datetime", "car")
    search_fields = ("user__email", "car__car_detail", "order_id")
    readonly_fields = ("order_id",)
    ordering = ("-start_datetime",)

    fieldsets = (
        (
            "Основное",
            {"fields": ("order_id", "user", "car")},
        ),
        (
            "Даты и Стоимость",
            {"fields": ("start_datetime", "end_datetime", "total_price")},
        ),
    )