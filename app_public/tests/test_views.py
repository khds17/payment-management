from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from app_public.models import Company, Address, Client as Tenant
from rest_framework import status
from datetime import timedelta, date
import json


class CreateCompanyTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.create_url = reverse('create')
        self.fake_user = {
            'name': 'FakeUser',
            'company_name': 'Fake Company',
            'email': 'fake@example.com',
            'password': 'password123',
            'phone': '12934567890',
            'cnpj': '12345678901230',
            'address': '123 Test St',
            'city': 'Test City',
            'state': 'Test State',
            'postalcode': '12345'
        }
        self.valid_payload = {
            'name': 'TestUser',
            'company_name': 'Test Company',
            'email': 'test@example.com',
            'password': 'password123',
            'phone': '12934567890',
            'cnpj': '31783287000105',
            'address': '123 Test St',
            'city': 'Test City',
            'state': 'Test State',
            'postalcode': '12345'
        }
        self.invalid_payload_missing_user_name = {
            'company_name': 'Test Company',
            'email': 'test@example.com',
            'password': 'password123',
            'phone': 1234567890,
            'cnpj': '12345678901230',
            'address': '123 Test St',
            'city': 'Test City',
            'state': 'Test State',
            'postalcode': '12345'
        }
        self.invalid_payload_missing_company_name = {
            'name': 'Test Company',
            'email': 'test@example.com',
            'password': 'password123',
            'phone': 1234567890,
            'cnpj': '12345678901230',
            'address': '123 Test St',
            'city': 'Test City',
            'state': 'Test State',
            'postalcode': '12345'
        }
        self.invalid_payload_missing_email = {
            'name': 'Test Company',
            'company_name': 'Test Company',
            'password': 'password123',
            'phone': 1234567890,
            'cnpj': '12345678901230',
            'address': '123 Test St',
            'city': 'Test City',
            'state': 'Test State',
            'postalcode': '12345'
        }
        self.invalid_payload_missing_password = {
            'name': 'Test Company',
            'company_name': 'Test Company',
            'email': 'test@example.com',
            'phone': 1234567890,
            'cnpj': '12345678901230',
            'address': '123 Test St',
            'city': 'Test City',
            'state': 'Test State',
            'postalcode': '12345'
        }
        self.invalid_payload_missing_cnpj = {
            'name': 'Test Company',
            'company_name': 'Test Company',
            'email': 'test@example.com',
            'password': 'password123',
            'phone': 1234567890,
            'address': '123 Test St',
            'city': 'Test City',
            'state': 'Test State',
            'postalcode': '12345'
        }
        self.invalid_payload_missing_phone = {
            'name': 'Test Company',
            'company_name': 'Test Company',
            'email': 'test@example.com',
            'password': 'password123',
            'cnpj': '12345678901230',
            'address': '123 Test St',
            'city': 'Test City',
            'state': 'Test State',
            'postalcode': '12345'
        }
        self.invalid_payload_missing_address = {
            'name': 'Test Company',
            'company_name': 'Test Company',
            'email': 'test@example.com',
            'password': 'password123',
            'phone': 1234567890,
            'city': 'Test City',
            'state': 'Test State',
            'postalcode': '12345'
        }
        self.invalid_payload_missing_city = {
            'name': 'TestUser',
            'company_name': 'Test Company',
            'email': 'test@example.com',
            'password': 'password123',
            'phone': '12934567890',
            'cnpj': '31783287000105',
            'address': '123 Test St',
            'state': 'Test State',
            'postalcode': '12345'
        }
        self.invalid_payload_missing_state = {
            'name': 'TestUser',
            'company_name': 'Test Company',
            'email': 'test@example.com',
            'password': 'password123',
            'phone': '12934567890',
            'cnpj': '31783287000105',
            'address': '123 Test St',
            'city': 'Test City',
            'postalcode': '12345'
        }
        self.invalid_payload_missing_postalcode = {
            'name': 'TestUser',
            'company_name': 'Test Company',
            'email': 'test@example.com',
            'password': 'password123',
            'phone': '12934567890',
            'cnpj': '31783287000105',
            'address': '123 Test St',
            'city': 'Test City',
            'state': 'Test State'
        }
        self.invalid_payload_existing_company_name = {
            'name': 'TestUser',
            'company_name': 'Fake Company',
            'email': 'test@example.com',
            'password': 'password123',
            'phone': 1234567890,
            'cnpj': '18400711000119',
            'address': '123 Test St',
            'city': 'Test City',
            'state': 'Test State',
            'postalcode': '12345'
        }
        self.invalid_payload_existing_cnpj = {
            'name': 'TestUser',
            'company_name': 'Test Company',
            'email': 'test@example.com',
            'password': 'password123',
            'phone': 1234567890,
            'cnpj': '12345678901230',
            'address': '123 Test St',
            'city': 'Test City',
            'state': 'Test State',
            'postalcode': '12345'
        }
        self.invalid_payload_existing_email = {
            'name': 'TestUser',
            'company_name': 'Test Company',
            'email': 'fake@example.com',
            'password': 'password123',
            'phone': 16988880000,
            'cnpj': '51353723000105',
            'address': '123 Test St',
            'city': 'Test City',
            'state': 'Test State',
            'postalcode': '12345'
        }
        
        self.client.post(
            self.create_url,
            data=json.dumps(self.fake_user),
            content_type='application/json'
        )

    def test_create_company_success(self):
        response = self.client.post(
            self.create_url,
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )

        user = User.objects.get(username='TestUser')
        company = Company.objects.get(name='Test Company')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Company.objects.count(), 2)
        self.assertEqual(company.name, 'Test Company')   
        self.assertEqual(company.cnpj, '31783287000105')
        self.assertEqual(company.phone, 12934567890)
        self.assertEqual(Address.objects.count(), 2)
        self.assertEqual(company.address.address, '123 Test St')
        self.assertEqual(company.address.city, 'Test City')
        self.assertEqual(company.address.state, 'Test State')
        self.assertEqual(company.address.postalcode, 12345)
        self.assertEqual(Tenant.objects.count(), 2)
        self.assertEqual(company.tenant.schema_name, 'test_company')
        self.assertEqual(company.tenant.name, 'Test Company')
        self.assertEqual(company.tenant.on_trial, True)
        self.assertEqual(company.tenant.paid_until, date.today()  + timedelta(days=13))
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(user.username, 'TestUser')
        self.assertEqual(user.first_name, 'TestUser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.is_active, True)
        self.assertEqual(response.data, 'Empresa cadastrada com sucesso')
        
    def test_create_company_missing_company_name(self):
        response = self.client.post(
            self.create_url,
            data=json.dumps(self.invalid_payload_missing_company_name),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Nome da empresa é obrigatório')
        
    def test_create_company_missing_user_name(self):
        response = self.client.post(
            self.create_url,
            data=json.dumps(self.invalid_payload_missing_user_name),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Nome do usuário é obrigatório')
                
    def test_create_company_missing_email(self):
        response = self.client.post(
            self.create_url,
            data=json.dumps(self.invalid_payload_missing_email),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'E-mail é obrigatório')
        
    def test_create_company_missing_password(self):
        response = self.client.post(
            self.create_url,
            data=json.dumps(self.invalid_payload_missing_password),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Senha é obrigatória')
        
    def test_create_company_missing_cnpj(self):
        response = self.client.post(
            self.create_url,
            data=json.dumps(self.invalid_payload_missing_cnpj),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'CNPJ é obrigatório')
        
    def test_create_company_missing_phone(self):
        response = self.client.post(
            self.create_url,
            data=json.dumps(self.invalid_payload_missing_phone),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Telefone é obrigatório')
        
    def test_create_company_missing_address(self):
        response = self.client.post(
            self.create_url,
            data=json.dumps(self.invalid_payload_missing_address),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Endereço é obrigatório')
        
    def test_create_company_missing_city(self):
        response = self.client.post(
            self.create_url,
            data=json.dumps(self.invalid_payload_missing_city),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Cidade é obrigatória')
        
    def test_create_company_missing_state(self):
        response = self.client.post(
            self.create_url,
            data=json.dumps(self.invalid_payload_missing_state),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Estado é obrigatório')
        
    def test_create_company_missing_postalcode(self):
        response = self.client.post(
            self.create_url,
            data=json.dumps(self.invalid_payload_missing_postalcode),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'CEP é obrigatório')

    def test_create_company_existing_company_name(self):
        response = self.client.post(
            self.create_url,
            data=json.dumps(self.invalid_payload_existing_company_name),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Nome da empresa já cadastrado')
        
    def test_create_company_existing_cnpj(self):
        response = self.client.post(
            self.create_url,
            data=json.dumps(self.invalid_payload_existing_cnpj),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'CNPJ já cadastrado')

    def test_create_company_existing_email(self):
        response = self.client.post(
            self.create_url,
            data=json.dumps(self.invalid_payload_existing_email),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'E-mail já cadastrado')
                
class EditCompanyTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.edit_url = reverse('edit')
        self.create_url = reverse('create')
        self.token_url = reverse('token')
        self.fake_user = {
            'name': 'FakeUser',
            'company_name': 'Fake Company',
            'email': 'fake@example.com',
            'password': 'password123',
            'phone': '12934567890',
            'cnpj': '12345678901230',
            'address': '123 Test St',
            'city': 'Test City',
            'state': 'Test State',
            'postalcode': '12345'
        }
        self.valid_payload = {
            'company_name': 'Updated Company',
            'cnpj': '31783287000105',
            'phone': '12934567890',
            'address': '456 Updated St',
            'city': 'Updated City',
            'state': 'Updated State',
            'postalcode': '67890'
        }
        self.invalid_payload = {
            'company_name': 'Invalid Company',
            'cnpj': '15203628000161',
            'phone': '12934567890',
            'address': '456 Updated St',
            'city': 'Updated City',
            'state': 'Updated State',
            'postalcode': '67890'
        }
        self.client.post(
            self.create_url,
            data=json.dumps(self.fake_user),
            content_type='application/json'
        ) 
        self.token = self.client.post(
            self.token_url,
            data=json.dumps({'email': 'fake@example.com', 'password': 'password123'}),
            content_type='application/json'
        )
            
    def test_edit_company_success(self):
        response = self.client.put(
            self.edit_url,
            data=json.dumps(self.valid_payload),
            content_type='application/json',
            headers={'Authorization': 'Token ' + self.token.data['token']}
        )   
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Empresa atualizada com sucesso')

    def test_edit_company_not_found(self):
        Company.objects.get().delete()
        
        response = self.client.put(
            self.edit_url,
            data=json.dumps(self.invalid_payload),
            content_type='application/json',
            HTTP_AUTHORIZATION='Token ' + self.token.data['token']
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], 'Empresa não encontrada')
        
class EditUserTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.edit_user_url = reverse('edit_user')
        self.create_url = reverse('create')
        self.token_url = reverse('token')
        self.fake_user = {
            'name': 'FakeUser',
            'company_name': 'Fake Company',
            'email': 'fake@example.com',
            'password': 'password123',
            'phone': '12934567890',
            'cnpj': '12345678901230',
            'address': '123 Test St',
            'city': 'Test City',
            'state': 'Test State',
            'postalcode': '12345'
        }
        self.valid_payload = {
            'name': 'UpdatedUser',
            'email': 'updated@example.com',
            'password': 'newpassword123',
            'status': False
        }
        self.invalid_payload_empty_name = {
            'name': '',
            'email': 'updated@example.com',
            'password': 'newpassword123',
            'is_active': True
        }
        self.invalid_payload_empty_email = {
            'name': 'UpdatedUser',
            'email': '',
            'password': 'newpassword123',
            'is_active': True
        }
        self.invalid_payload_empty_password = {
            'name': 'UpdatedUser',
            'email': 'updated@example.com',
            'password': '',
            'is_active': True
        }
        self.invalid_payload_empty_status = {
            'name': 'UpdatedUser',
            'email': 'updated@example.com',
            'password': 'newpassword123',
            'status': ''
        }
        
        self.client.post(
            self.create_url,
            data=json.dumps(self.fake_user),
            content_type='application/json'
        )
        self.token = self.client.post(
            self.token_url,
            data=json.dumps({'email': 'fake@example.com', 'password': 'password123'}),
            content_type='application/json'
        )

    def test_edit_user_success(self):
        response = self.client.put(
            self.edit_user_url,
            data=json.dumps(self.valid_payload),
            content_type='application/json',
            HTTP_AUTHORIZATION='Token ' + self.token.data['token']
        )
               
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Usuário atualizada com sucesso')