from django.urls import path
from .import views

urlpatterns = [
    path('service/create', views.create_service, name='create_service'),
    path('service/get', views.get_all_services, name='get_all_services'),
    path('service/edit', views.edit_service, name='edit_service'),
    path('plan/create', views.create_plan, name='create_plan'),
    path('plan/get', views.get_all_plans, name='get_all_plans'),
]
