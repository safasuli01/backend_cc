from django.urls import path
from .views import *

urlpatterns = [
    path('projects/', project_list, name='project_list'),  # Lists all projects, or creates a new projects
     path('projects/<int:id>/', project_detail, name='project_detail'),
    path('projects/<int:id>/update/', project_update, name='project_update'),  # Updates a specific project
    path('projects/<int:id>/delete/', project_delete, name='project_delete'),  # Deletes a specific project
]
