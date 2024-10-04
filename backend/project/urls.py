from django.urls import path
from .views import ProjectCreateView, ProjectListView, ProjectDetailView

urlpatterns = [
    path('create/', ProjectCreateView.as_view(), name='project-create'),  # URL to create a project
    path('list/', ProjectListView.as_view(), name='project-list'),        # URL to list all projects by a company
    path('<int:project_id>/', ProjectDetailView.as_view(), name='project-detail'),  # URL to get, update, or delete a specific project
]
