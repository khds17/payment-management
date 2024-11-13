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
    
def get_tenant(data):
    
    user_company = UserCompany.objects.get(user=data)
    
    company = Company.objects.get(id=user_company.company.id)
    
    tenant = Client.objects.get(id=company.tenant_id)
        
    return tenant
    