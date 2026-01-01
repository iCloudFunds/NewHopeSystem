from django.contrib import admin
from core.models.parents import ParentProfile, ParentLoginLog

@admin.register(ParentProfile)
class ParentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number')
    filter_horizontal = ('students',)

@admin.register(ParentLoginLog)
class ParentLoginLogAdmin(admin.ModelAdmin):
    list_display = ('parent', 'login_time', 'ip_address')