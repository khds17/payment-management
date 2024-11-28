from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from app_public.models import UserCompany, Company, Client
import json
import random


@api_view(['POST'])
def create_token(request):
    user = get_object_or_404(User, email=request.data['email'])
    
    if not user.check_password(request.data['password']):
        return Response('Senha incorreta', status.HTTP_404_NOT_FOUND)

    token, created = Token.objects.get_or_create(user=user)     
        
    return Response({'token': token.key}, status.HTTP_201_CREATED)

def get_company(data):
    try: 
        user_company = UserCompany.objects.get(user=data)
    
        company = Company.objects.get(id=user_company.company.id)
    
        return company
    except UserCompany.DoesNotExist:
        return None
    
def get_tenant(data):
    
    user_company = UserCompany.objects.get(user=data)
    
    company = Company.objects.get(id=user_company.company.id)
    
    tenant = Client.objects.get(id=company.tenant_id)
        
    return tenant

def json_load(request):
    try :
        data = json.loads(request.body)
        return data
    except json.JSONDecodeError:
        return Response({'error': 'Nenhum dado foi enviado'}, status=status.HTTP_400_BAD_REQUEST)
    
def delete_created_objects(tenant=None, address=None, company=None, user=None):
    if tenant:
        tenant.delete()
    if address:
        address.delete()
    if company:
        company.delete()
    if user:
        user.delete()
        
def generate_username(name):
    username = name.replace(' ', '_').lower()
    random_number = random.randint(1000, 9999)
    username = f"{username}_{random_number}"
    return username