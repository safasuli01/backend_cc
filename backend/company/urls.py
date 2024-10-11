from django.urls import path
from .views import *

urlpatterns = [
    path('register/', CompanyRegistrationView.as_view(), name='company-registration'),  # Added parentheses here
    path('activate/<uidb64>/', activate, name='activate-company'),  # Ensure this matches with the send_activation_email
    path('search/', search_company, name='company-search'),
    path('list/', list_company, name='company-list'),
]
