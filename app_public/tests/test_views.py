from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from ..models import Company, Address, UserCompany, Client as Tenant
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
        self.invalid_payload_cnpj = {
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
        self.invalid_payload_email = {
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

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, 'Empresa cadastrada com sucesso')

    def test_create_company_existing_cnpj(self):
        response = self.client.post(
            self.create_url,
            data=json.dumps(self.invalid_payload_cnpj),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, 'CNPJ existente')

    def test_create_company_existing_email(self):
        response = self.client.post(
            self.create_url,
            data=json.dumps(self.invalid_payload_email),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, 'E-mail existente')

class CreateTokenTestCase(TestCase):
            def setUp(self):
                self.client = Client()
                self.token_url = reverse('token')
                self.user = User.objects.create_user(
                    username='testuser',
                    email='testuser@example.com',
                    password='password123'
                )

            def test_create_token_success(self):
                response = self.client.post(
                    self.token_url,
                    data=json.dumps({'email': 'testuser@example.com', 'password': 'password123'}),
                    content_type='application/json'
                )
                self.assertEqual(response.status_code, status.HTTP_201_CREATED)
                self.assertIn('token', response.data)

            def test_create_token_invalid_password(self):
                response = self.client.post(
                    self.token_url,
                    data=json.dumps({'email': 'testuser@example.com', 'password': 'wrongpassword'}),
                    content_type='application/json'
                )
                self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
                self.assertEqual(response.data, 'Senha incorreta')

            def test_create_token_nonexistent_user(self):
                response = self.client.post(
                    self.token_url,
                    data=json.dumps({'email': 'nonexistent@example.com', 'password': 'password123'}),
                    content_type='application/json'
                )
                self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
class EditCompanyTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.edit_url = reverse('edit')
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
        
        self.client.post(
            self.create_url,
            data=json.dumps(self.fake_user),
            content_type='application/json'
        )

    def test_edit_company_success(self):
        valid_payload = {
            'company_name': 'Updated Company',
            'cnpj': '31783287000105',
            'phone': '12934567890',
            'address': '456 Updated St',
            'city': 'Updated City',
            'state': 'Updated State',
            'postalcode': '67890'
        }
        response = self.client.put(
            self.edit_url,
            data=json.dumps(valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Empresa atualizada com sucesso')

    def test_edit_company_not_found(self):
        self.company.delete()
        response = self.client.put(
            self.edit_url,
            data=json.dumps({}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], 'Empresa não encontrada')

    # def test_edit_address_not_found(self):
    #     self.address.delete()
    #     response = self.client.put(
    #         self.edit_url,
    #         data=json.dumps({}),
    #         content_type='application/json'
    #     )
    #     self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    #     self.assertEqual(response.data['error'], 'Endereço não encontrado')

    # def test_edit_company_invalid_data(self):
    #     invalid_payload = {
    #         'company_name': '',
    #         'cnpj': 'invalid_cnpj',
    #         'phone': 'invalid_phone',
    #         'address': '',
    #         'city': '',
    #         'state': '',
    #         'postalcode': ''
    #     }
    #     response = self.client.put(
    #         self.edit_url,
    #         data=json.dumps(invalid_payload),
    #         content_type='application/json'
    #     )
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

                
                
