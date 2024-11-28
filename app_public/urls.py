from django.urls import path
from .import views
import core.utils as utils

urlpatterns = [
    path('create', views.create_company, name='create'),
    path('token', utils.create_token, name='token'),
    path('edit', views.edit_company, name='edit'),
    path('user/edit', views.edit_user, name='edit_user'),
]
