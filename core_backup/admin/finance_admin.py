from django.contrib import admin
from core.models.finance import FeePayment, PaymentMethodConfig

@admin.register(FeePayment)
class FeePaymentAdmin(admin.ModelAdmin):
    list_display = ('student', 'amount_paid', 'reference_number', 'date_paid')
    search_fields = ('reference_number', 'student__student_id')

@admin.register(PaymentMethodConfig)
class PaymentMethodConfigAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_enabled')