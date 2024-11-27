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
from core.utils import get_company

import json


# Verificar o pq não cadastra usuário com mesmo nome
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
                
    tenant_data = {
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
        return Response({'error': 'CNPJ já cadastrado'}, status.HTTP_400_BAD_REQUEST)
    
    if Client.objects.filter(name=company_name).exists():
        return Response({'error': 'Nome da empresa já cadastrado'}, status.HTTP_400_BAD_REQUEST)
    
    if User.objects.filter(email=email).exists():
        return Response({'error': 'E-mail já cadastrado'}, status.HTTP_400_BAD_REQUEST)
  
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
                return Response(address_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                  
            company_data = {
                'name': company_name,
                'cnpj': cnpj,
                'phone': phone,
                'tenant': tenant.id,
                'address': address.id,
            }
                                        
            company_serializer = CompanySerializer(data=company_data)
            if company_serializer.is_valid():
                company = company_serializer.save()
            else:
                return Response(company_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                        
            user_serializer = UserSerializer(data=user_data)           
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
        return Response({'error': str(e)}, status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# E se passar request.body sem nenhum parâmetro?
@api_view(['PUT'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def edit_company(request):    
    try :
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return Response({'error': 'Nenhum dado foi enviado'}, status=status.HTTP_400_BAD_REQUEST)
    
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
    
# def edit_user(request):
#     data = json.loads(request.body)
#     user = User.objects.get(id=data['id'])
#     serializer = UserSerializer(user, data=data)
    
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   

