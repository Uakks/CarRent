from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Register your models here.
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    ordering = ('email', )
    list_display = ('email', 'full_name', 'is_staff')
    list_filter = ('full_name',)
    search_fields = ('email', 'full_name')
    readonly_fields = ('id', 'created_at', 'updated_at', 'deleted_at',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}), 
        ("Personal_info", {'fields': ("full_name",)}), 
        ("Permissions", {'fields': ('is_active', 'is_staff', 'is_superuser')}), 
        ("Important dates", {'fields': ('last_login',)}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
