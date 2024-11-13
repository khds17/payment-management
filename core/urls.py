from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('company/', include('app_public.urls')),
    path('', include('app_client.urls')),
]
