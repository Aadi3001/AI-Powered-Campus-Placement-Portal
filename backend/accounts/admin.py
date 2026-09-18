from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class CustomUserAdmin(UserAdmin):
    """
    Extends Django's built-in UserAdmin so the 'role' field
    is visible and editable in the admin panel.
    """
    fieldsets = UserAdmin.fieldsets + (
        ('Role Info', {'fields': ('role',)}),
    )
    list_display = ('username', 'email', 'role', 'is_staff')


admin.site.register(User, CustomUserAdmin)