from django.contrib import admin
from django.contrib.admin import ModelAdmin
# Register your models here.
from .models import Car

class CarAdmin(ModelAdmin):
    ordering = ('price_per_day', )   # сначала дешёвые машины, потом дорогие
    list_display = ('price_per_day', 'model', 'year')  
    # Какие колонки видны в списке: цена, модель, год
    list_filter = ('price_per_day',)   # можно выбрать цену и увидеть только такие машины
    search_fields = ('price_per_day', 'model')  # Строка поиска сверху
    readonly_fields = ('car_id', 'created_at', 'updated_at', 'deleted_at')
    fieldsets = (
        (None, {'fields': ('owner', 'model', 'year')}),
        ("Price", {'fields': ('price_per_day', 'is_available')}),
    )

admin.site.register(Car, CarAdmin)