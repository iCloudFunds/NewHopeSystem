from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from core.models.users import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Role Identification', {'fields': ('is_student', 'is_teacher', 'is_parent')}),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')