from django.urls import path
from .views import JobCreateView, JobListView, JobDetailView

urlpatterns = [
    path('create/', JobCreateView.as_view(), name='job-create'),  # URL to create a job
    path('list/', JobListView.as_view(), name='job-list'),        # URL to list all jobs by a company
    path('<int:job_id>/', JobDetailView.as_view(), name='job-detail'),  # URL to get, update, or delete a specific job
]
