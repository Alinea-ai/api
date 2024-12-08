from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model

from .models import (
    Entity,
    AccessRequest,
    AccessRequestItem,
    Visits,
    Template,
    DefaultField, UserTemplateAssignment,
)

User = get_user_model()  # This returns your CustomUser model

class CustomUserAdmin(BaseUserAdmin):
    model = User
    list_display = ('id', 'username', 'email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('id', 'username', 'email', 'first_name', 'last_name')
    ordering = ('id',)
    # If you have custom fields, add them to fieldsets
    fieldsets = BaseUserAdmin.fieldsets + (
        (None, {'fields': ('phone_number',)}),
    )

# No need to unregister; just register your custom user model
admin.site.register(User, CustomUserAdmin)

# Register other models
admin.site.register(Entity)
admin.site.register(AccessRequest)
admin.site.register(AccessRequestItem)
admin.site.register(Visits)
admin.site.register(Template)
admin.site.register(DefaultField)

@admin.register(UserTemplateAssignment)
class UserTemplateAssignmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'template', 'entity', 'assigned_at', 'status')
    search_fields = ('user__username', 'template__name', 'entity__name')
    list_filter = ('status', 'assigned_at', 'entity')
    ordering = ('entity', 'user', 'template')
