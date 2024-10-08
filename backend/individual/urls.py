# from django.urls import path
# from individual import views
# from rest_framework.urlpatterns import format_suffix_patterns
#
# urlpatterns = [
#     # Lists all individuals or creates a new individual
#     path('', views.list_individual, name='individual-list-create'),
#
#     # Get, update, or delete a specific individual by ID
#     path('<int:id>/', views.individual_detail, name='individual-detail'),
#
#     # Login view for user authentication
#     path('login/', views.user_login_view, name='user-login'),
# ]
#
# # Add support for suffix patterns like '.json', '.api', etc.
# urlpatterns = format_suffix_patterns(urlpatterns)

from django.urls import path
from .views import *

urlpatterns = [
    path('register/', IndividualRegistrationView.as_view(), name='individual-registration'),  # Added parentheses here
    path('activate/<uidb64>/', activate, name='activate-individual'),  # Ensure this matches with the send_activation_email
    path('search/', search_individual, name='individual-search'),
    path('list/', list_individual, name='individual-list'),
    path('update/<int:id>/', individual_update, name='individual-update'),
    path('delete/<int:id>/', individual_delete, name='individual-delete'),

]
# id here will be the individual id 