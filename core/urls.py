from django.urls import path
from . import views


urlpatterns = [
    path('dropdowns/manage/', views.manage_dropdowns, name='manage_dropdowns'),
    path('dropdowns/<str:model_key>/<int:pk>/update/', views.update_field, name='update_field'),
    path('dropdowns/<str:model_key>/<int:pk>/delete/', views.delete_field, name='delete_field'),

]

