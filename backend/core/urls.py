
from django.contrib import admin
from django.urls import path, include
from authentication.views import *
from individual.views import *
from company.views import *
from django.contrib.auth import views as auth_views


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
    #reset password
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    #OTP
    path('otp/send-otp/', SendOTPView.as_view(), name='send_otp'),
    path('otp/verify-otp/', VerifyOTPView.as_view(), name='verify_otp'),
]
