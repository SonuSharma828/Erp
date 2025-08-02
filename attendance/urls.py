from django.urls import path
from . import views

urlpatterns = [
    path('', views.attendance_list, name='attendance_list1'),
    path('mark/', views.mark_attendance, name='mark_attendance'),
    path('edit/<int:pk>/', views.edit_attendance, name='edit_attendance'),
    path('report/<int:user_id>/', views.monthly_report, name='monthly_attendance_report'),

]

