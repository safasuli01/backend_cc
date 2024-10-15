from django.urls import path
from .views import *

urlpatterns = [
    path('register/', CompanyRegistrationView.as_view(), name='company-registration'),  # Added parentheses here
    path('activate/<uidb64>/', activate, name='activate-company'),  # Ensure this matches with the send_activation_email
    path('search/', search_company, name='company-search'),
    path('list/', list_company, name='company-list'),
    path('update/<int:id>/', company_update, name='company-update'),
    path('delete/<int:id>/', company_delete, name='company-delete'),

    path('profile/', get_company_profile, name='company-profile'),# For the logged-in company's profile
    path('profile/<int:id>/', get_company_profile, name='company-detail'),  # For viewing any company by ID
    
    ]
