from django.contrib import admin
from .models import (
    Entity,
    AccessRequest,
    AccessRequestItem,
    UserPersonalInformation,
    UserMedicalInfo,
    DentalInfo,
    PsychologicalInfo,
    MedicalRecord,
)

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

class UserAdmin(BaseUserAdmin):
    list_display = ('id', 'username', 'email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('id', 'username', 'email', 'first_name', 'last_name')

admin.site.unregister(User)
admin.site.register(User, UserAdmin)


admin.site.register(Entity)
admin.site.register(AccessRequest)
admin.site.register(AccessRequestItem)
admin.site.register(UserPersonalInformation)
admin.site.register(UserMedicalInfo)
admin.site.register(DentalInfo)
admin.site.register(PsychologicalInfo)
admin.site.register(MedicalRecord)
