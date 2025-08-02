from django.urls import path, include
from . import views 


app_name = 'employee'

urlpatterns = [
    path('employee/', views.employees, name='employee'),
    path('employee/add/', views.add_employee, name='add_employee'),
    path('employee/edit/<int:pk>/', views.edit_employee, name='edit_employee'),
    path('employee/delete/<int:pk>/', views.delete_employee, name='delete_employee'),
    path('<int:pk>/', views.employee_detail, name='employee_detail'),
] 
