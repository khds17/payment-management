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

import json
from datetime import datetime, timedelta, date


def find(request):
    try:
        if request.GET.get('id'):
            id = request.GET.get('id')
            
            try:
                company = Company.objects.get(id=id)
                serializer = CompanySerializer(company)
                return Response(serializer.data)
            except Company.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)

#Verificar o pq não cadastra usuário com mesmo nome
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

    
def edit(request):
    data = json.loads(request.body)
    company = Company.objects.get(id=data['id'])
    serializer = CompanySerializer(company, data=data)
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def delete(request):
    try:
        if request.GET.get('id'):
            id = request.GET.get('id')
            
            try:
                company = Company.objects.get(id=id)
                company.delete()
            except Company.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
   
@api_view(['POST']) 
def login(request):
    data = json.loads(request.body)
    email = data.get('email')
    password = data.get('password')
    
    user = auth.authenticate(
        request,
        username=email,
        password=password
    )
        
    if user is None:
        return Response("Login failed", status.HTTP_401_UNAUTHORIZED)
    
    auth.login(request, user)
    session_key = request.session.session_key
    
    return JsonResponse({
        "message": "Login successful",
        "session_key": session_key
    }, status=status.HTTP_200_OK)

@api_view(['POST']) 
def logout(request):
    auth.logout(request)
    return Response("Logout successful")

@api_view(['GET'])
@login_required
def get_tenant(request):
    schema = get_tenant_model()
    print(schema)
    # return Response(schema.schema_name)


    
    







