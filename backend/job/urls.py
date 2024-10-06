from django.urls import path
from .views import *

urlpatterns = [
    path('create/', job_create, name='job_create'),
    path('all/', job_list, name='job_list'),  # Lists all jobs, or creates a new job
    path('<int:id>/', job_detail, name='job_detail'),
    path('<int:id>/update/', job_update, name='job_update'),  # Updates a specific job
    path('<int:id>/delete/', job_delete, name='job_delete'),  # Deletes a specific job
    path('search/', search_job, name='search_job'),
]


