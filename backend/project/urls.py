from django.urls import path

from .views import *

urlpatterns = [
    path('create/', project_create, name='project_create' ),
    path('all/', project_list, name='project_list'),  # Lists all projects, or creates a new projects
    path('<int:id>/', project_detail, name='project_detail'),
    path('<int:id>/update/', project_update, name='project_update'),  # Updates a specific project
    path('<int:id>/delete/', project_delete, name='project_delete'),  # Deletes a specific project
]

