from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from base.models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = (
        "username", "email", "first_name", "last_name", "is_active",
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(id=request.user.id)

    def has_change_permission(self, request, obj=None):
        has_permission = super().has_change_permission(request, obj)
        if not has_permission:
            return False
        if obj is not None and not request.user.is_superuser:
            return obj.id == request.user.id
        return True

    def has_add_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser
