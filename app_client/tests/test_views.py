from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
import json


class CreateServiceTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.create_service_url = reverse('create_service')
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
            'name': 'Test Service',
            'description': 'Test Description'
        }
        self.invalid_payload_existing_name = {
            'name': 'Test Service',
            'description': 'Another Description'
        }
        self.invalid_payload_missing_name = {
            'description': 'Test Description'
        }
        
        self.client.post(
            self.create_url,
            data=json.dumps(self.fake_user),
            content_type='application/json'
        )
        
        self.token_url = reverse('token')
        self.token = self.client.post(
            self.token_url,
            data=json.dumps({'email': 'fake@example.com', 'password': 'password123'}),
            content_type='application/json'
        )

    def test_create_service_success(self):
        response = self.client.post(
            self.create_service_url,
            data=json.dumps(self.valid_payload),
            content_type='application/json',
            headers={'Authorization': f"Token {self.token.data['token']}"}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, 'Serviço cadastrado com sucesso')

    def test_create_service_existing_name(self):
        self.client.post(
            self.create_service_url,
            data=json.dumps(self.valid_payload),
            content_type='application/json',
            headers={'Authorization': f"Token {self.token.data['token']}"}
        )
        response = self.client.post(
            self.create_service_url,
            data=json.dumps(self.invalid_payload_existing_name),
            content_type='application/json',
            headers={'Authorization': f"Token {self.token.data['token']}"}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, 'Serviço com nome existente')

    def test_create_service_missing_name(self):
        response = self.client.post(
            self.create_service_url,
            data=json.dumps(self.invalid_payload_missing_name),
            content_type='application/json',
            headers={'Authorization': f"Token {self.token.data['token']}"}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)

    def test_create_service_wrong_token(self):
        response = self.client.post(
            self.create_service_url,
            data=json.dumps(self.valid_payload),
            content_type='application/json',
            headers={'Authorization': 'Token 3be1db43f5107736135956946f4a35f1031fba82'}
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['detail'], 'Invalid token.')

