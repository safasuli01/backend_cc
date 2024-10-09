# from django.urls import path
# from company import views
#
# urlpatterns = [
#     # URL for listing and creating companies
#     path('', views.list_company, name='company-list-create'),
#
#     # URL for retrieving a specific company by ID
#     path('<int:id>/', views.company_detail, name='company-detail'),
#
#     # URL for updating a specific company by ID
#     path('<int:id>/update/', views.update_company, name='company-update'),
#
#     # URL for deleting a specific company by ID
#     path('<int:id>/delete/', views.delete_company, name='company-delete'),
#
#     # URL for user login (if needed separately)
#     path('login/', views.company_login_view, name='company-login'),
#
#     # Search for companies
#     path('search/', views.search_company, name='company-search'),  # Search URL
# ]

from django.urls import path
from .views import *

urlpatterns = [
    path('register/', CompanyRegistrationView.as_view(), name='company-registration'),  # Added parentheses here
    path('activate/<uidb64>/', activate, name='activate-company'),  # Ensure this matches with the send_activation_email
    path('search/', search_company, name='company-search'),
    path('list/', list_company, name='company-list'),
    path('update/<int:id>/', company_update, name='company-update'),
    path('delete/<int:id>/', company_delete, name='company-delete'),
]
# id here will be the company id 