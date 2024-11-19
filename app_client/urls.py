from django.urls import path
from .import views

urlpatterns = [
    path('service/create', views.create_service, name='create_service'),
    path('service/find', views.get_all_services, name='get_all_services'),
    path('service/edit', views.edit_service, name='edit_service'),
    path('plan/create', views.create_plan, name='create_plan'),
    path('plan/find', views.get_all_plans, name='get_all_plans'),
    path('plan/edit', views.edit_plan, name='edit_plan'),
    path('plan/service/find', views.get_all_plan_services, name='get_all_plan_services'),
    path('plan/service/add', views.add_service_to_plan, name='add_service_to_plan'),
]
