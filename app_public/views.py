from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from .models import *
from django.contrib.auth.models import User
from .serializer import *
from datetime import timedelta, date
from core.utils import get_company, json_load, delete_created_objects, generate_username, validate_required_fields


@api_view(['POST'])
def create_company(request):
    data = json_load(request)  
    
    required_fields = ['company_name', 'name', 'email', 'password', 'address', 'city', 'state', 'postalcode', 'phone', 'cnpj']
    validation_error = validate_required_fields(data, required_fields)
    if validation_error:
        return validation_error   
    
    schema_name = data['company_name'].replace(' ', '_').lower()
    
    username = generate_username(data['name'])

    tenant_data = {
        'schema_name': schema_name,
        'name': data['company_name'],
        'paid_until': date.today()  + timedelta(days=13),
        'on_trial': True
    }
    
    user_data = {
        'first_name': data['name'],
        'username': username,
        'is_active': True,
        'email': data['email'],
        'password': data['password']
    }
    
    address_data = {
        'address': data['address'],
        'city': data['city'],
        'state': data['state'],
        'postalcode': data['postalcode']
    }
    
    if Company.objects.filter(cnpj=data['cnpj']).exists():
        return Response({'error': 'CNPJ already registered'}, status.HTTP_400_BAD_REQUEST)
    
    if Client.objects.filter(name=data['company_name']).exists():
        return Response({'error': 'Company name already registered'}, status.HTTP_400_BAD_REQUEST)
    
    if User.objects.filter(email=data['email']).exists():
        return Response({'error': 'E-mail already registered'}, status.HTTP_400_BAD_REQUEST)
  
    try:
        with transaction.atomic():
            tenant_serializer = ClientSerializer(data=tenant_data)            
            if tenant_serializer.is_valid():
                tenant = tenant_serializer.save()
            else:
                return Response(tenant_serializer.errors, status.HTTP_400_BAD_REQUEST)
                        
            address_serializer = AddressSerializer(data=address_data)
            if address_serializer.is_valid():
                address = address_serializer.save()
            else:
                delete_created_objects(tenant=tenant)
                return Response(address_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                    
            company_data = {
                'name': data['company_name'],
                'cnpj': data['cnpj'],
                'phone': data['phone'],
                'tenant': tenant.id,
                'address': address.id,
            }
                                        
            company_serializer = CompanySerializer(data=company_data)
            if company_serializer.is_valid():
                company = company_serializer.save()
            else:
                delete_created_objects(tenant=tenant, address=address)
                return Response(company_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                        
            user_serializer = UserSerializer(data=user_data)           
            if user_serializer.is_valid():
                user = user_serializer.save()
            else:
                delete_created_objects(tenant=tenant, address=address, company=company)
                return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            user_company_serializer = UserCompanySerializer(data={
                'user': user.id,
                'company': company.id
            })
            
            if user_company_serializer.is_valid():
                user_company_serializer.save()
            else:
                delete_created_objects(tenant=tenant, address=address, company=company, user=user)
                return Response(user_company_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        return Response('Empresa cadastrada com sucesso', status.HTTP_201_CREATED)
    except Exception as e:
        delete_created_objects(tenant=tenant, address=address, company=company, user=user)
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def edit_company(request):    
    data = json_load(request)
    
    company_name = data.get('company_name')
    cnpj = data.get('cnpj')
    phone = data.get('phone')
    address = data.get('address')
    city = data.get('city')
    state = data.get('state')
    postalcode = data.get('postalcode')

    company_data = {
        'name': company_name,
        'cnpj': cnpj,
        'phone': phone,
    }

    address_data = {
        'address': address,
        'city': city,
        'state': state,
        'postalcode': postalcode
    }
    
    company = get_company(request.user.id)        
        
    if company is None:
        return Response({'error': 'Empresa não encontrada'}, status=status.HTTP_404_NOT_FOUND)
    
    address = Address.objects.get(id=company.address_id)
    
    if address is None:
        return Response({'error': 'Endereço não encontrado'}, status=status.HTTP_404_NOT_FOUND)
            
    try:                
        with transaction.atomic():
            company_serializer = CompanySerializer(company, data=company_data, partial=True)
            if company_serializer.is_valid():
                company_serializer.save()
            else:
                return Response(company_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            address_serializer = AddressSerializer(address, data=address_data, partial=True)
            if address_serializer.is_valid():
                address_serializer.save()
            else:
                return Response(address_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            return Response({'message': 'Empresa atualizada com sucesso'}, status=status.HTTP_200_OK)    
    except ValueError as e:
        return Response({'error': str(e)}, status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def edit_user(request):
    data = json_load(request)
          
    user = User.objects.get(id=request.user.id)
    
    user_data = {
        'username': data.get('name'),
        'first_name': data.get('name'),
        'email': data.get('email'),
        'password': data.get('password'),
        'is_active': data.get('status')
    }
       
    user_serializer = UserSerializer(user, data=user_data, partial=True)
    
    if user_serializer.is_valid():
        user_serializer.save()
        return Response({'message': 'Usuário atualizada com sucesso'}, status=status.HTTP_200_OK)   
    return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


   

