from django.urls import path
from . import views

urlpatterns = [
    path('', views.knowledge_list, name='knowledge_list'),
    path('add/', views.add_knowledge, name='add_knowledge'),
    path('edit/<int:pk>/', views.edit_knowledge, name='edit_knowledge'),
    path('delete/<int:pk>/', views.delete_knowledge, name='delete_knowledge'),
]