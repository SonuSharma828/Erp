from django.urls import path
from . import views

urlpatterns = [
    path('', views.task_group_list, name='task_group_list'),
    path('add/', views.add_task_group, name='add_task_group'),
    path('delete/<int:sno>/', views.delete_task_group, name='delete_task_group'),
    path('edit/<int:sno>/', views.edit_task_group, name='edit_task_group'),
]