from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from ..models import Company, Address, UserProfile, Client as Tenant
import json
from datetime import datetime, timedelta


class CreateCompanyTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('create_company')
        self.valid_payload = {
            'name': 'Test User',
            'company_name': 'Test Company',
            'email': 'test@example.com',
            'password': 'password123',
            'phone': '1234567890',
            'cnpj': '12345678901234',
            'address': '123 Test St',
            'city': 'Test City',
            'state': 'Test State',
            'postalcode': '12345'
        }
        self.invalid_payload_cnpj = {
            'name': 'Test User',
            'company_name': 'Test Company',
            'email': 'test@example.com',
            'password': 'password123',
            'phone': '1234567890',
            'cnpj': 'existing_cnpj',
            'address': '123 Test St',
            'city': 'Test City',
            'state': 'Test State',
            'postalcode': '12345'
        }
        self.invalid_payload_email = {
            'name': 'Test User',
            'company_name': 'Test Company',
            'email': 'existing@example.com',
            'password': 'password123',
            'phone': '1234567890',
            'cnpj': '12345678901234',
            'address': '123 Test St',
            'city': 'Test City',
            'state': 'Test State',
            'postalcode': '12345'
        }
        Company.objects.create(cnpj='existing_cnpj')
        User.objects.create_user(username='existing_user', email='existing@example.com', password='password123')

    def test_create_company_success(self):
        response = self.client.post(
            self.url,
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Company.objects.count(), 2)
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(Address.objects.count(), 1)
        self.assertEqual(UserProfile.objects.count(), 1)
        self.assertEqual(Tenant.objects.count(), 1)

    def test_create_company_existing_cnpj(self):
        response = self.client.post(
            self.url,
            data=json.dumps(self.invalid_payload_cnpj),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, 'CNPJ existente')

    def test_create_company_existing_email(self):
        response = self.client.post(
            self.url,
            data=json.dumps(self.invalid_payload_email),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, 'E-mail existente')