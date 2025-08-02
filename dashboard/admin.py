from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    readonly_fields = ['auto_link_info']
    fieldsets = UserAdmin.fieldsets + (
        ("Additional Info", {'fields': ('department', 'employee', 'auto_link_info')}),
    )

    def auto_link_info(self, obj):
        if obj.employee:
            return f"Auto-linked to: {obj.employee.name}"
        return "No linked employee yet"
    auto_link_info.short_description = "Employee Link Status"

admin.site.register(CustomUser, CustomUserAdmin) 
