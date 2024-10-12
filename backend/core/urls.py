from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/individual/', include('individual.urls')),
    path('api/company/', include('company.urls')),
    path('api/auth/', include('authentication.urls')),
    path('api/project/', include('project.urls')),
    path('api/job/', include('job.urls')),
    path('api/application/', include('application.urls')),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)