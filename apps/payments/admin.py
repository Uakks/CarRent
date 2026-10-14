from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin) :
    list_display = (
        'payment_id',
        'order',
        'total_price',
        'start_datetime',
        'paid_at',
        'created_at',
    )
    list_filter = ('paid_at','start_datetime', 'created_at')
    search_fields = ('payment_id','order__order_id')
    readonly_fields = ('payment_id','created_at','updated_at','deleted_at')