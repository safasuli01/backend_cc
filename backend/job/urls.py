from django.urls import path
from .views import *

urlpatterns = [
    path('jobs/', job_list, name='job_list'),  # Lists all jobs, or creates a new job
     path('jobs/<int:id>/', job_detail, name='job_detail'),
    path('jobs/<int:id>/update/', job_update, name='job_update'),  # Updates a specific job
    path('jobs/<int:id>/delete/', job_delete, name='job_delete'),  # Deletes a specific job
]


