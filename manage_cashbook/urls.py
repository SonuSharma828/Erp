from django.urls import path
from . import views

urlpatterns = [
    path('', views.cashbook_list, name='cashbook_list'),
    path('add/', views.add_cashbook_entry, name='add_cashbook_entry'),
    path('edit/<int:entry_id>/', views.edit_cashbook_entry, name='edit_cashbook_entry'),
    path('delete/<int:entry_id>/', views.delete_cashbook_entry, name='delete_cashbook_entry'),
]