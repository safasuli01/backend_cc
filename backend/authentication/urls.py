from django.urls import path
from .views import *

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('logout/', UserLogoutView.as_view(), name='user-logout'),
    path('detail/', UserDetailView.as_view(), name='user-detail'),
    path('csrf/', get_csrf_token),
]