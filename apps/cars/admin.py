from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.admin import ModelAdmin
# Register your models here.
from .models import Car

class CarAdmin(ModelAdmin):
    ordering = ('price_per_day', )
    list_display = ('price_per_day', 'model', 'year')
    list_filter = ('price_per_day',)
    search_fields = ('price_per_day', 'model')
    readonly_fields = ('car_id', 'created_at', 'updated_at', 'deleted_at', 'owner')
    fieldsets = (
        (None, {'fields': ('model', 'year')}), 
        ("Price", {'fields': ("price_per_day",)}), 
    )

admin.site.register(Car, CarAdmin)