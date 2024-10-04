
from django.contrib import admin
from django.urls import path, include
from authentication.views import *
from individual.views import *
from company.views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    #auth
    path('api/auth/register', UserRegistrationView.as_view(), name='user-registration'),
    path('api/auth/login/', UserLoginView.as_view(), name='user-login'),
    path('api/auth/logout', UserLogoutView.as_view(), name='user-logout'),
    #individual
    path('api/auth/register/individual/', IndividualRegistrationView.as_view(), name='individual-registration'),
    #company
    path('api/auth/register/company/', CompanyRegistrationView.as_view(), name='company-registration'),
    #job
    path('api/job/', include('job.urls')),

]
