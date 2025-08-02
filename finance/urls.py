from django.urls import path
from . import views

urlpatterns = [
    path('add-income/', views.add_income, name='add_income'),
    path('add-expense/', views.add_expense, name='add_expense'),
    path('add-salary-payment/', views.add_salary_payment, name='add_salary_payment'),
    path('finance/', views.finance_summary, name='finance'),
    path('export-finance-csv/', views.export_finance_csv, name='export_finance_csv'),
    path('export-finance-pdf/', views.export_finance_pdf, name='export_finance_pdf'),
]