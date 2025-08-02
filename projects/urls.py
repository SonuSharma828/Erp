from django.urls import path
from . import views

app_name = 'project'

urlpatterns = [
    path('project/', views.project, name='project'),
    path('project/add/', views.add_project, name='add_project'),
    path('project/edit/<int:pk>', views.edit_project, name='edit_project'),
    path('project/delete/<int:pk>', views.delete_project, name='delete_project'),
    #path('project/view/<int:pk>', views.view_project, name='view_project'),
    #path('project/add_task/<int:pk>', views.add_task, name='add_task'),
    #path('project/add_comment/<int:pk>', views.add_comment, name='add_comment'),
    #path('project/mark_task_complete/<int:task_id>', views.mark_task_complete, name='mark_task_complete'),
    #path('project/delete_task/<int:task_id>', views.delete_task, name='delete_task'),
    #path('project/delete_comment/<int:comment_id>', views.delete_comment, name='delete_comment'),
    path('ajax/customers/', views.paginated_customers, name='ajax_customers'),

]
