from django.shortcuts import render
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from .models import *
from django.contrib.auth.models import User
from .serializer import CompanySerializer
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django_tenants.utils import get_tenant_model
from django.http import JsonResponse

import json
from datetime import datetime, timedelta


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def company(request):
    if request.method == 'GET':
        find(request)
        
    if request.method == 'POST':
        response = create(request)
        return Response(response.status_code)
    
    if request.method == 'PUT':
        edit(request)
    
    if request.method == 'DELETE':
        delete(request)
            
    return Response(status=status.HTTP_400_BAD_REQUEST)

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

@csrf_exempt
def create(request):
    data = json.loads(request.body)
    
    name = data.get('name')
    company_name = data.get('company_name')
    email = data.get('email')
    password = data.get('password')
    phone = data.get('phone')
    cnpj = data.get('cnpj')
    address = data.get('address')
    city = data.get('city')
    state = data.get('state')
    postalcode = data.get('postalcode')
    
    company_name = company_name.lower().replace(' ', '_')
    
    if Company.objects.filter(cnpj=cnpj).exists():
        return Response('CNPJ existente', status.HTTP_400_BAD_REQUEST)
    
    if User.objects.filter(email=email).exists():
        return Response('E-mail existente', status.HTTP_400_BAD_REQUEST)
  
    try:
        with transaction.atomic():
            tenant = Client(
                schema_name=company_name,
                name=company_name,
                paid_until=datetime.now() + timedelta(days=13),
                on_trial=True
            )
            tenant.save()
  
            address = Address(
                address=address,
                city=city,
                state=state,
                postalcode=postalcode,
            )  
            address.save()
                                        
            company = Company(
                name=company_name,
                cnpj=cnpj,
                phone=phone,
                tenant_id=tenant.id,
                address_id=address.id,
            )
            company.save()
            
            user = User.objects.create_user(
                first_name=name,
                username=name,
                is_active=True,
                email=email,
                password=password,
            )
            user.save()
                                   
            user_company = UserCompany(
                user_id=user.id,
                company_id=company.id
            )   
            user_company.save()
            
        return Response('Account created', status.HTTP_201_CREATED)
    except ValueError as e:
        return Response({'error': str(e)}, status.HTTP_400_BAD_REQUEST)

    
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


    
    







