from django.contrib import admin
from .models import (
    SparePart,
    SparePartTransaction,
    Voucher,
    MonthlySale,
    MonthlyExpense,
    MonthlyVendorPayment
)

@admin.register(SparePart)
class SparePartAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'quantity', 'purchase_price', 'selling_price', 'created_at')
    search_fields = ('name', 'category')
    list_filter = ('category',)

@admin.register(SparePartTransaction)
class SparePartTransactionAdmin(admin.ModelAdmin):
    list_display = ('sparepart', 'transaction_type', 'quantity', 'amount', 'payment_mode', 'transaction_date')
    search_fields = ('sparepart__name', 'transaction_type')
    list_filter = ('transaction_type', 'payment_mode', 'transaction_date')

@admin.register(Voucher)
class VoucherAdmin(admin.ModelAdmin):
    list_display = ('voucher_type', 'amount', 'transaction_date', 'payment_mode')
    list_filter = ('voucher_type', 'transaction_date')

@admin.register(MonthlySale)
class MonthlySaleAdmin(admin.ModelAdmin):
    list_display = ('date', 'amount', 'description','product','invoice_number')
    list_filter = ('product', 'date')

@admin.register(MonthlyExpense)
class MonthlyExpenseAdmin(admin.ModelAdmin):
    list_display = ('date', 'amount', 'expense_type', 'description')
    list_filter = ('expense_type', 'date')

@admin.register(MonthlyVendorPayment)
class MonthlyVendorPaymentAdmin(admin.ModelAdmin):
    list_display = ('vendor_name', 'date', 'amount', 'description')
    list_filter = ('vendor_name', 'date')
