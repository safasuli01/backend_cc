# from django.conf.urls.static import static
# from django.contrib import admin
# from django.urls import path, include
# from authentication.views import *
# from individual.views import *
# from company.views import *
# from django.contrib.auth import views as auth_views
# from django.conf import settings
#
# urlpatterns = [
#     path('admin/', admin.site.urls),
#     #auth
#     path('register', UserRegistrationView.as_view(), name='user-registration'),
#     path('login/', UserLoginView.as_view(), name='user-login'),
#     path('logout', UserLogoutView.as_view(), name='user-logout'),
#
#     #individual
#     # path('api/auth/register/individual/', IndividualRegistrationView.as_view(), name='individual-registration'),
#     path('individual/', include('individual.urls')),
#     #company
#     path('company/', include('company.urls')),
#
#     #job
#     path('job/', include('job.urls')),
#
#     #project
#     path('project/', include('project.urls')),
#
#     #reset password
#     path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
#     path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
#     path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
#     path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
#
#     #OTP
#     path('otp/send-otp/', SendOTPView.as_view(), name='send_otp'),
#     path('otp/verify-otp/', VerifyOTPView.as_view(), name='verify_otp'),
#
# ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/individual/', include('individual.urls')),
    path('api/company/', include('company.urls')),
    path('api/auth/', include('authentication.urls')),
    path('project/', include('project.urls')),
    path('job/', include('job.urls')),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)