from django.urls import path
from . import views

urlpatterns = [
    path('', views.department_list, name='department_list'),
    path('add/', views.add_department, name='add_department'),
    path('delete/<int:sno>/', views.delete_department, name='delete_department'),
    path('edit/<int:sno>/', views.edit_department, name='edit_department'),
    path('users/', views.user_list, name='user_list'),
    path('users/create/', views.user_create, name='user_create'),
    path('users/edit/<int:pk>/', views.user_edit, name='user_edit'),
    path('users/delete/<int:pk>/', views.user_delete, name='user_delete'),
    path('payments/', views.payment_list, name='payment_list'),
    path('payments/add/', views.add_payment, name='add_payment'),
    path('payments/edit/<int:pk>/', views.edit_payment, name='edit_payment'),
    path('payments/delete/<int:pk>/', views.delete_payment, name='delete_payment'),
    path('payments/pending/', views.pending_payments_list, name='pending_payments_list'),
    path('payments/<int:pk>/approve/', views.approve_payment, name='approve_payment'),
    path('payments/<int:pk>/reject/', views.reject_payment, name='reject_payment'),
    path('employee-payment-dashboard/', views.employee_payment_dashboard, name='employee_payment_dashboard'),
    path('employee-payment-chart-data/', views.employee_payment_chart_data, name='employee_payment_chart_data'),
    path('export-employee-payment-csv/', views.export_employee_payment_csv, name='export_employee_payment_csv'),


]



from django.urls import path
from . import views

urlpatterns += [
    
    path('leaves/', views.leave_list, name='leave-list'),
    path('leaves/apply/', views.leave_apply, name='leave-apply'),
    path('leaves/review/<int:pk>/', views.leave_review, name='leave-review'),

    path('attendance-report/', views.attendance_report_view, name='attendance_report'),
    path('apply-leave/', views.leave_apply_view, name='apply_leave'),
    path('leave-requests/', views.leave_requests_view, name='leave_requests'),
    path('leave-report/', views.leave_report_view, name='leave_report'),
]

