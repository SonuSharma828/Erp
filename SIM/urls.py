from django.urls import path
from . import views

urlpatterns = [
    path('daily-status/', views.daily_status_list, name='daily_status_list'),
    path('daily-status/add/', views.add_daily_status, name='add_daily_status'),
    path('daily-status/edit/<int:pk>/', views.edit_daily_status, name='edit_daily_status'),
    path('daily-status/delete/<int:pk>/', views.delete_daily_status, name='delete_daily_status'),
    path('payment-followup/', views.payment_followup_list, name='payment_followup_list'),
    path('payment-followup/add/', views.add_payment_followup, name='add_payment_followup'),
    path('payment-followup/edit/<int:pk>/', views.edit_payment_followup, name='edit_payment_followup'),
    path('payment-followup/delete/<int:pk>/', views.delete_payment_followup, name='delete_payment_followup'),
    path('quick-jobs/', views.quickjob_list, name='quickjob_list'),
    path('quick-jobs/add/', views.add_quickjob, name='add_quickjob'),
    path('quick-jobs/edit/<int:pk>/', views.edit_quickjob, name='edit_quickjob'),
    path('quick-jobs/delete/<int:pk>/', views.delete_quickjob, name='delete_quickjob'),
    path('simjobs/', views.simjob_list, name='simjob_list'),
    path('simjobs/add/', views.simjob_add, name='simjob_add'),
    path('simjobs/edit/<int:pk>/', views.simjob_edit, name='simjob_edit'),
    path('simjobs/delete/<int:pk>/', views.simjob_delete, name='simjob_delete'),
    path('expenses/', views.expense_list, name='expense_list'),
    path('expenses/add/', views.add_expense, name='add_expense'),
    path('expenses/bulk-approve/', views.bulk_approve_expenses, name='bulk_approve_expenses'),
    path('hp-summary/', views.hp_summary, name='hp_summary'),

]
