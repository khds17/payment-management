from django.urls import path
from .import views

urlpatterns = [
    path('create', views.create_company, name='create'),
    path('token', views.create_token, name='token'),
]
