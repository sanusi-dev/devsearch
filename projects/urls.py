from django.urls import path
from .views import *

urlpatterns = [
    path('projects/', project_list, name='project_list'),
    path('project/<str:pk>/', project_detail, name='project_detail'),
    path('create-project/', project_create, name='project_create'),
    path('update-project/<str:pk>/', update_project, name='update_project'),
    path('delete-project/<str:pk>/', delete_project, name='delete_project'),
]
