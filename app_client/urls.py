from django.urls import path
from .import views

urlpatterns = [
    path('service/create', views.create_service, name='create_service'),
]
