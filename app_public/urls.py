from django.urls import path
from .import views

urlpatterns = [
    path('create', views.create_company, name='create'),
    path('token', views.create_token, name='token'),
    path('edit', views.edit_company, name='edit'),
]
