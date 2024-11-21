from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from .models import *
from django.contrib.auth.models import User
from .serializer import *
from django.shortcuts import get_object_or_404
from rest_framework.authtoken.models import Token
from datetime import timedelta, date

import json


#Verificar o pq não cadastra usuário com mesmo nome
# Verificar se está criptografando a senha
# Está criando o tenant mesmo com erro.
@api_view(['POST'])
def create_company(request):
    data = json.loads(request.body)
    
    company_name = data.get('company_name')
    schema_name = data.get('company_name')
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    address = data.get('address')
    city = data.get('city')
    state = data.get('state')
    postalcode = data.get('postalcode')
    phone = data.get('phone')
    cnpj = data.get('cnpj')
    
    if company_name is None:
        return Response({'error': 'Nome da empresa é obrigatório'}, status.HTTP_400_BAD_REQUEST)
    
    if name is None:
        return Response({'error': 'Nome do usuário é obrigatório'}, status.HTTP_400_BAD_REQUEST)
    
    if email is None:
        return Response({'error': 'E-mail é obrigatório'}, status.HTTP_400_BAD_REQUEST)
    
    if password is None:
        return Response({'error': 'Senha é obrigatória'}, status.HTTP_400_BAD_REQUEST)
    
    if address is None:
        return Response({'error': 'Endereço é obrigatório'}, status.HTTP_400_BAD_REQUEST)
    
    if city is None:
        return Response({'error':'Cidade é obrigatória'}, status.HTTP_400_BAD_REQUEST)
    
    if state is None:
        return Response({'error': 'Estado é obrigatório'}, status.HTTP_400_BAD_REQUEST)
    
    if postalcode is None:
        return Response({'error': 'CEP é obrigatório'}, status.HTTP_400_BAD_REQUEST)
    
    if phone is None:
        return Response({'error': 'Telefone é obrigatório'}, status.HTTP_400_BAD_REQUEST)
    
    if cnpj is None:
        return Response({'error': 'CNPJ é obrigatório'}, status.HTTP_400_BAD_REQUEST)
    
    schema_name = schema_name.replace(' ', '_').lower()
                
    company_data = {
        'schema_name': schema_name,
        'name': company_name,
        'paid_until': date.today()  + timedelta(days=13),
        'on_trial': True
        }
    
    user_data = {
        'first_name': name,
        'username': name,
        'is_active': True,
        'email': email,
        'password': password
        }
    
    address_data = {
        'address': address,
        'city': city,
        'state': state,
        'postalcode': postalcode
    }
    
    if Company.objects.filter(cnpj=cnpj).exists():
        return Response('CNPJ existente', status.HTTP_400_BAD_REQUEST)
    
    if Client.objects.filter(schema_name=company_name).exists():
        return Response('Nome da empresa existente', status.HTTP_400_BAD_REQUEST)
    
    if User.objects.filter(email=email).exists():
        return Response('E-mail existente', status.HTTP_400_BAD_REQUEST)
  
    try:
        with transaction.atomic():
            tenant_serializer = ClientSerializer(data=company_data)
            tenant = None
            
            if tenant_serializer.is_valid():
                tenant = tenant_serializer.save()
            else:
                return Response(tenant_serializer.errors, status.HTTP_400_BAD_REQUEST)
                        
            address_serializer = AddressSerializer(data=address_data)
            address = None
            
            if address_serializer.is_valid():
                address = address_serializer.save()
            else:
                return Response(address_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                  
            company_data = {
                'name': company_name,
                'cnpj': cnpj,
                'phone': phone,
                'tenant': tenant.id,
                'address': address.id,
            }
                                        
            company_serializer = CompanySerializer(data=company_data)
            company = None
            if company_serializer.is_valid():
                company = company_serializer.save()
            else:
                return Response(company_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                        
            user_serializer = UserSerealizer(data=user_data)
            user = None
            
            if user_serializer.is_valid():
                user = user_serializer.save()
            else:
                return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            user_company_serializer = UserCompanySerializer(data={
                'user': user.id,
                'company': company.id
            })
            
            if user_company_serializer.is_valid():
                user_company_serializer.save()
            else:
                return Response(user_company_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        return Response('Empresa cadastrada com sucesso', status.HTTP_201_CREATED)
    except ValueError as e:
        return Response(e, status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def edit_company(request):
    try:
        company = get_company(request.user.id)
        address = Address.objects.get(id=company.address_id)
    except Company.DoesNotExist:
        return Response({'error': 'Empresa não encontrada'}, status=status.HTTP_404_NOT_FOUND)
    except Address.DoesNotExist:
        return Response({'error': 'Endereço não encontrado'}, status=status.HTTP_404_NOT_FOUND)
    
    data = request.data

    # Manually update the fields
    company.name = data.get('company_name', company.name)
    company.cnpj = data.get('cnpj', company.cnpj)
    company.phone = data.get('phone', company.phone)
    address.address = data.get('address', address.address)
    address.city = data.get('city', address.city)   
    address.state = data.get('state', address.state)
    address.postalcode = data.get('postalcode', address.postalcode)

    try:
        company.save()
        address.save()
        return Response({'message': 'Empresa atualizada com sucesso'},
        status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

def edit_user(request):
    data = json.loads(request.body)
    user = User.objects.get(id=data['id'])
    serializer = UserSerealizer(user, data=data)
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   
@api_view(['POST'])
def create_token(request):
    user = get_object_or_404(User, email=request.data['email'])
    
    if not user.check_password(request.data['password']):
        return Response('Senha incorreta', status.HTTP_404_NOT_FOUND)

    token, created = Token.objects.get_or_create(user=user)     
        
    return Response({'token': token.key}, status.HTTP_201_CREATED)

def get_company(data):
    
    user_company = UserCompany.objects.get(user=data)
    
    company = Company.objects.get(id=user_company.company.id)
    
    return company
