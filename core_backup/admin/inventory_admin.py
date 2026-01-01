from django.contrib import admin
from core.models.inventory import Asset, Issuance

@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ('item_name', 'total_quantity')

@admin.register(Issuance)
class IssuanceAdmin(admin.ModelAdmin):
    list_display = ('asset', 'student', 'date_issued', 'returned')