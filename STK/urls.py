from django.urls import path
from . import views

urlpatterns = [
    # STK Units
    path('units/', views.unit_list, name='unit_list'),
    path('units/add/', views.unit_add, name='unit_add'),
    path('units/edit/<int:pk>/', views.unit_edit, name='unit_edit'),
    path('units/delete/<int:pk>/', views.unit_delete, name='unit_delete'),

    # STK Categories
    path('categories/', views.category_list, name='category_list'),
    path('categories/add/', views.category_add, name='category_add'),
    path('categories/edit/<int:pk>/', views.category_edit, name='category_edit'),
    path('categories/delete/<int:pk>/', views.category_delete, name='category_delete'),

    # STK Items
    path('stocks/', views.stock_list, name='stock_list'),
    path('stocks/add/', views.stock_add, name='stock_add'),
    path('stocks/edit/<int:pk>/', views.stock_edit, name='stock_edit'),
    path('stocks/delete/<int:pk>/', views.stock_delete, name='stock_delete'),
    path('stock/<int:pk>/', views.stock_detail, name='stock_detail'),


    # STK Take
    path('take/', views.take_list, name='take_list'),
    path('take/add/', views.take_add, name='take_add'),
    path('take/edit/<int:pk>/', views.take_edit, name='take_edit'),
    path('take/delete/<int:pk>/', views.take_delete, name='take_delete'),
]
