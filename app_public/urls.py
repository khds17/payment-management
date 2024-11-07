from django.urls import path
from .import views

urlpatterns = [
    path('create', views.create_company, name='create'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('get_tenant', views.get_tenant, name='get_tenant'),
]
