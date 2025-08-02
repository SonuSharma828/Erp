from django.urls import path
from . import views

urlpatterns = [
    path('', views.task_list, name='task_list'),
    path('add/', views.add_task, name='add_task'),
    path('edit/<int:sno>/', views.edit_task, name='edit_task'),
    path('delete/<int:sno>/', views.delete_task, name='delete_task'),
    path('task-earning-dashboard/', views.task_earning_dashboard, name='task_earning_dashboard'),
    path('task-earning-chart-data/', views.task_earning_chart_data, name='task_earning_chart_data'),
    path('export-task-earning-csv/', views.export_task_earning_csv, name='export_task_earning_csv'),

]

urlpatterns += [
    path('service/', views.service_charge_list, name='service-charges-list'),
    path('service/edit/<int:pk>/', views.service_charge_edit, name='service-charge-edit'),
    path('service/delete/<int:pk>/', views.service_charge_delete, name='service-charge-delete'),
]
