from django.test import TestCase, Client
from django.contrib.auth.models import User
from rest_framework import status
from django.urls import reverse
import json


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