from django.urls import path
from individual import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    # Lists all individuals or creates a new individual
    path('', views.list_individual, name='individual-list-create'),

    # Get, update, or delete a specific individual by ID
    path('<int:id>/', views.individual_detail, name='individual-detail'),

    # Login view for user authentication
    path('login/', views.user_login_view, name='user-login'),
]

# Add support for suffix patterns like '.json', '.api', etc.
urlpatterns = format_suffix_patterns(urlpatterns)
