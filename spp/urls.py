from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.spp_dashboard, name='spp_dashboard'),
    path('finance-summary/', views.get_finance_summary, name='finance-summary'),
    path('spareparts/', views.manage_spareparts, name='manage_spareparts'),
    path('add-transaction/', views.add_transaction, name='add_transaction'),
    path('export-csv/', views.export_csv, name='export_csv'),
    path('create-voucher/', views.create_voucher, name='create_voucher'),
    path('voucher-history/', views.voucher_history, name='voucher_history'),
    path('edit-voucher/<int:pk>/', views.edit_voucher, name='edit_voucher'),
    path('delete-voucher/<int:pk>/', views.delete_voucher, name='delete_voucher'),
    path('manage-sales/', views.manage_sales, name='manage_sales'),
    path('manage-expenses/', views.manage_expenses, name='manage_expenses'),
    path('manage-vendor-payments/', views.manage_vendor_payments, name='manage_vendor_payments'),
    # Sales
    path('edit-sales/<int:pk>/', views.edit_sales, name='edit_sales'),
    path('delete-sales/<int:pk>/', views.delete_sales, name='delete_sales'),
    path('add-sales/', views.add_sales, name='add_sales'),
    path('sales-dashboard/', views.sales_dashboard, name='sales_dashboard'),
    path('sales-chart-data/', views.sales_chart_data, name='sales_chart_data'),
    path('export-sales-csv/', views.export_sales_csv, name='export_sales_csv'),

    # Expenses
    path('edit-expense/<int:pk>/', views.edit_expense, name='edit_expense'),
    path('delete-expense/<int:pk>/', views.delete_expense, name='delete_expense'),
    path('add-expense/', views.add_expenses, name='add_expenses'),
    path('total-expense-dashboard/', views.total_expense_dashboard, name='total_expense_dashboard'),
    path('total-expense-chart-data/', views.total_expense_chart_data, name='total_expense_chart_data'),
    path('export-expense-csv/', views.export_expense_csv, name='export_expense_csv'),

    # Vendor Payments
    path('edit-vendor-payment/<int:pk>/', views.edit_vendor_payment, name='edit_vendor_payment'),
    path('delete-vendor-payment/<int:pk>/', views.delete_vendor_payment, name='delete_vendor_payment'),
    path('add-vendor-payment/', views.add_vendor_payments, name='add_vendor_payment'),
    path('vendor-payment-dashboard/', views.vendor_payment_dashboard, name='vendor_payment_dashboard'),
    path('vendor-payment-chart-data/', views.vendor_payment_chart_data, name='vendor_payment_chart_data'),
    path('export-vendor-payment-csv/', views.export_vendor_payment_csv, name='export_vendor_payment_csv'),


]
