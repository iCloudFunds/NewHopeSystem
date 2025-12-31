from django.contrib import admin
from core.models.controls import ModuleControl

@admin.register(ModuleControl)
class ModuleControlAdmin(admin.ModelAdmin):
    list_display = ('module_name', 'is_active')