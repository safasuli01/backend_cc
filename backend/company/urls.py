from django.urls import path
from company import views

urlpatterns = [
    # URL for listing and creating companies
    path('', views.list_company, name='company-list-create'),
    
    # URL for retrieving a specific company by ID
    path('<int:id>/', views.company_detail, name='company-detail'),
    
    # URL for updating a specific company by ID
    path('<int:id>/update/', views.update_company, name='company-update'),
    
    # URL for deleting a specific company by ID
    path('<int:id>/delete/', views.delete_company, name='company-delete'),

    # URL for user login (if needed separately)
    path('login/', views.company_login_view, name='company-login'),
    
    # Search for companies
    path('search/', views.search_company, name='company-search'),  # Search URL    
]
