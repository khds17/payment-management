from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializer import *
from django.db import transaction 
from .models import *
from app_public.models import *
from django_tenants.utils import schema_context
import json 


@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_service(request):  
    try:
        tenant = get_tenant(request.user.id)
    except Client.DoesNotExist:
        return Response({'error': 'Usuário não encontrado'}, status=status.HTTP_404_NOT_FOUND)
    
    data = json.loads(request.body)
        
    name = data.get('name')
    description = data.get('description')
    
    service = {
        'name': name,
        'description': description,
    }
    
    with schema_context(tenant.schema_name):
        if Service.objects.filter(name=name).exists():
            return Response('Serviço com nome existente', status.HTTP_400_BAD_REQUEST)  
    
        try:
            with transaction.atomic():
                service_serializer = ServiceSerializer(data=service)
                
                if service_serializer.is_valid():
                    service_serializer.save()
                else:
                    return Response(service_serializer.errors, status.HTTP_400_BAD_REQUEST)
            return Response('Serviço cadastrado com sucesso', status.HTTP_201_CREATED)
        except ValueError as e:
            return Response(e, status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_all_services(request):
    tenant = get_tenant(request.user.id)
    id = request.data.get('name')
    
    with schema_context(tenant.schema_name):
        services = Service.objects.all()

        service_serializer = ServiceSerializer(services, many=True)

        return Response(service_serializer.data, status=status.HTTP_200_OK)
    
@api_view(['PUT'])    
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def edit_service(request):
    data = json.loads(request.body)
    
    tenant = get_tenant(request.user.id)
    
    id = data.get('id')
    name = data.get('name')
    description = data.get('description')
    service_status = data.get('status')
    
    service = {
        'name': name,
        'description': description,
        'status': service_status
    }
    
    with schema_context(tenant.schema_name):
        try:
            service = Service.objects.get(id=id)
        except Service.DoesNotExist:
            return Response('Serviço não encontrado', status=status.HTTP_404_NOT_FOUND)
        
        service_serializer = ServiceSerializer(service, data=data)

        if service_serializer.is_valid():
            service_serializer.save()
            return Response('Serviço alterado com sucesso', status=status.HTTP_200_OK)
        else:
            return Response(service_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])        
def create_plan(request):
    data = json.loads(request.body)
    tenant = get_tenant(request.user.id)
    plan_name = data.get('name')
    plan_description = data.get('description')
    
    if plan_name is None:
        return Response('Nome do plano é obrigatório', status.HTTP_400_BAD_REQUEST)
        
    plan_data = {
        'name': plan_name,
        'description': plan_description,
    }
    
    plan_services_data = data.get('services')
    
    if plan_services_data is None:
        return Response('Serviços são obrigatórios', status.HTTP_400_BAD_REQUEST)
               
    with schema_context(tenant.schema_name):    
        if Plan.objects.filter(name=plan_name).exists():
            return Response('Plano com nome existente', status.HTTP_400_BAD_REQUEST)  
        
        try:
            with transaction.atomic():
                plan_serializer = PlanSerializer(data=plan_data)
                
                if plan_serializer.is_valid():
                    plan = plan_serializer.save()
                else:
                    return Response(plan_serializer.errors, status.HTTP_400_BAD_REQUEST)
                           
                for service in plan_services_data:  
                    service_id = service.get('id')
                    price = service.get('price')
                    quantity = service.get('quantity')
                    description = service.get('description')
                    total = round(price * quantity, 2)

                    try:
                        service = Service.objects.get(id=service_id)
                    except Service.DoesNotExist:
                        return Response({'error': 'Serviço não encontrado'}, status=status.HTTP_404_NOT_FOUND)

                    if price is None or quantity is None:
                        return Response({'error': 'Preço e quantidade são obrigatórios'}, status=status.HTTP_400_BAD_REQUEST)
                    
                    PlanService.objects.create(
                        price=price,
                        quantity=quantity,
                        total=total,
                        description=description,
                        plan=plan,
                        service=service
                    )
        except ValueError as e:
            return Response(e, status.HTTP_404_NOT_FOUND)
        
    return Response('Plano cadastrado com sucesso', status.HTTP_201_CREATED)

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_all_plans(request):
    tenant = get_tenant(request.user.id)
    
    with schema_context(tenant.schema_name):
        plans = Plan.objects.all()

        plan_serializer = PlanSerializer(plans, many=True)

        return Response(plan_serializer.data, status=status.HTTP_200_OK)
    
@api_view(['PUT'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])    
def edit_plan(request):
    data = json.loads(request.body)
    
    tenant = get_tenant(request.user.id)
    
    id = data.get('id')
    name = data.get('name')
    description = data.get('description')
    
    plan = {
        'name': name,
        'description': description,
    }
    
    with schema_context(tenant.schema_name):
        try:
            plan = Plan.objects.get(id=id)
        except Plan.DoesNotExist:
            return Response('Plano não encontrado', status=status.HTTP_404_NOT_FOUND)
        
        plan_serializer = PlanSerializer(plan, data=data)

        if plan_serializer.is_valid():
            plan_serializer.save()
            return Response('Plano alterado com sucesso', status=status.HTTP_200_OK)
        else:
            return Response(plan_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def get_tenant(data):
    
    user_company = UserCompany.objects.get(user=data)
    
    company = Company.objects.get(id=user_company.company.id)
    
    tenant = Client.objects.get(id=company.tenant_id)
        
    return tenant
    