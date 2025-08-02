from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.technician_dashboard, name='technician_dashboard'),
    path('tasks/', views.technician_task_list, name='technician_task_list'),
    path('tasks/<int:task_id>/', views.technician_task_detail, name='technician_task_detail'),
    path('leave/apply/', views.technician_leave_apply, name='technician-leave-apply'),
    path('leave/list/', views.technician_leave_list, name='technician-leave-list'),
]

