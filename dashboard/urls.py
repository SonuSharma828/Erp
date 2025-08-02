from django.urls import path,include
from django.contrib import admin
from . import views

urlpatterns = [
    #path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    #path('signup/', views.signup_page, name='signup'),
    path('create-user/', views.create_user_view, name='create_user'),
    path('users/', views.user_list_view, name='luser_list'),
    path('users/edit/<int:user_id>/', views.edit_user_view, name='edit_user'),
    path('users/delete/<int:user_id>/', views.delete_user_view, name='delete_user'),
   
    path('employee/', include('employees.urls', namespace='employee')),
    path('project/', include('projects.urls', namespace='project')),
    #path('inventory/', include('inventory.urls',namespace='inventory')),
    #path('report/', include('reports.urls',namespace='report')),
    #path('finance/', include('finance.urls')),
    path('task-group/', include('task_group.urls')),
    path('tasks/', include('manage_tasks.urls')),
    path('cashbook/', include('manage_cashbook.urls')),
    path('knowledge/', include('knowledge_base.urls')),
    path('customers/', include('customer.urls')),
    path('supplier/', include('supplier.urls')),
    path('spp/', include('spp.urls')),
    path('HRM/', include('HRM.urls')),
    path('SIM/', include('SIM.urls')),
    path('STK/', include('STK.urls')),
    path('technician/', include('technician.urls')),
    path('attendance/', include('attendance.urls')),
    path('core/', include('core.urls')),
    path('api/', include('api.urls')),
    path('select2/', include('django_select2.urls')),
]



# urls.py

urlpatterns += [
    path('companies/', views.company_list, name='company_list'),
    path('companies/add/', views.add_company, name='add_company'),
    path('companies/edit/<int:pk>/', views.edit_company, name='edit_company'),
    path('companies/delete/<int:pk>/', views.delete_company, name='delete_company'),

    path('invoices/', views.invoice_list, name='invoice_list'),
    path('invoices/create/', views.create_invoice, name='create_invoice'),
    path('invoices/edit/<int:pk>/', views.edit_invoice, name='edit_invoice'),
    path('invoices/delete/<int:pk>/', views.delete_invoice, name='delete_invoice'),
]

