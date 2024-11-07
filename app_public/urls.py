from django.urls import path
from .import views

urlpatterns = [
    path('api/company', views.company, name='company'),
    path('api/login', views.login, name='login'),
    path('api/logout', views.logout, name='logout'),
    path('api/get_tenant', views.get_tenant, name='get_tenant'),
]
