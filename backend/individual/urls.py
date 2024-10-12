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