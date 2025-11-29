
from django.contrib import admin
from .models import Payment
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('txn_id', 'merchant', 'upi_id', 'amount', 'created_at', 'payment_status')
    list_filter = ('merchant', 'created_at', 'payment_status')
    search_fields = ('txn_id', 'merchant', 'upi_id')
    ordering = ('-created_at',)
