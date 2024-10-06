from django.urls import path
from company import views

urlpatterns = [
    # URL for listing and creating companies
    path('', views.list_company, name='company-list-create'),

    # URL for retrieving, updating, and deleting a specific company by ID
    path('<int:id>/', views.company_detail, name='company-detail'),

    # URL for user login (if needed separately)
    path('login/', views.UserLoginView.as_view(), name='company-login'),
]
