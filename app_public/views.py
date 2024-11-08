from django.shortcuts import render
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from .models import *
from django.contrib.auth.models import User
from .serializer import *
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django_tenants.utils import get_tenant_model
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.authtoken.models import Token
from datetime import timedelta, date

import json


#Verificar o pq não cadastra usuário com mesmo nome
# Verificar se está criptografando a senha
@api_view(['POST'])
def create_company(request):
    data = json.loads(request.body)
    
    company_name = data.get('company_name').lower().replace(' ', '_')
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    address = data.get('address')
    city = data.get('city')
    state = data.get('state')
    postalcode = data.get('postalcode')
    phone = data.get('phone')
    cnpj = data.get('cnpj')
            
    company_data = {
        'schema_name': company_name,
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

    
def edit_company(request):
    data = json.loads(request.body)
    company = Company.objects.get(id=data['id'])
    serializer = CompanySerializer(company, data=data)
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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





    
    







