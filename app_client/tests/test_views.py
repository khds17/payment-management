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
        self.assertEqual(response.data['error'], 'Serviço com nome existente')

    def test_create_service_missing_name(self):
        response = self.client.post(
            self.create_service_url,
            data=json.dumps(self.invalid_payload_missing_name),
            content_type='application/json',
            headers={'Authorization': f"Token {self.token.data['token']}"}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Nome do serviço é obrigatório')

    def test_create_service_wrong_token(self):
        response = self.client.post(
            self.create_service_url,
            data=json.dumps(self.valid_payload),
            content_type='application/json',
            headers={'Authorization': 'Token 3be1db43f5107736135956946f4a35f1031fba82'}
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['detail'], 'Invalid token.')

class GetAllServicesTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.create_service_url = reverse('create_service')
        self.get_all_services_url = reverse('get_all_services')
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
        self.service_one = {
            'name': 'Test Service 1',
            'description': 'Test Description'
        }
        self.service_two = {
            'name': 'Test Service 2',
            'description': 'Another Description'
        }
        self.service_three = {
            'name': 'Test Service 3',
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
        
        self.client.post(
            self.create_service_url,
            data=json.dumps(self.service_one),
            content_type='application/json',
            headers={'Authorization': f"Token {self.token.data['token']}"}
        )
        
        self.client.post(
            self.create_service_url,
            data=json.dumps(self.service_two),
            content_type='application/json',
            headers={'Authorization': f"Token {self.token.data['token']}"}
        )
        
        self.client.post(
            self.create_service_url,
            data=json.dumps(self.service_three),
            content_type='application/json',
            headers={'Authorization': f"Token {self.token.data['token']}"}
        )

    def test_get_all_services_success(self):
        response = self.client.get(
            self.get_all_services_url,
            content_type='application/json',
            headers={'Authorization': f"Token {self.token.data['token']}"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)

    def test_get_all_services_wrong_token(self):
        response = self.client.get(
            self.get_all_services_url,
            content_type='application/json',
            headers={'Authorization': 'Token 3be1db43f5107736135956946f4a35f1031fba82'}
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['detail'], 'Invalid token.')
        
class EditServiceTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.create_service_url = reverse('create_service')
        self.edit_service_url = reverse('edit_service')
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
        self.service = {
            'name': 'Test Service',
            'description': 'Test Description'
        }
        self.valid_payload = {
            'id': 1,
            'name': 'Updated Service',
            'description': 'Updated Description',
            'status': 'false'
        }
        self.invalid_payload_missing_id = {
            'name': 'Updated Service',
            'description': 'Updated Description',
            'status': 'active'
        }
        self.invalid_payload_missing_name = {
            'id': 1,
            'description': 'Updated Description',
            'status': 'active'
        }
        self.invalid_payload_nonexistent_id = {
            'id': 999,
            'name': 'Nonexistent Service',
            'description': 'Nonexistent Description',
            'status': 'active'
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
        
        self.client.post(
            self.create_service_url,
            data=json.dumps(self.service),
            content_type='application/json',
            headers={'Authorization': f"Token {self.token.data['token']}"}
        )

    def test_edit_service_success(self):
        response = self.client.put(
            self.edit_service_url,
            data=json.dumps(self.valid_payload),
            content_type='application/json',
            headers={'Authorization': f"Token {self.token.data['token']}"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, 'Serviço alterado com sucesso')
        
    def test_edit_service_missing_id(self):
        response = self.client.put(
            self.edit_service_url,
            data=json.dumps(self.invalid_payload_missing_id),
            content_type='application/json',
            headers={'Authorization': f"Token {self.token.data['token']}"}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'ID do serviço é um campo obrigatório')

    def test_edit_service_missing_name(self):
        response = self.client.put(
            self.edit_service_url,
            data=json.dumps(self.invalid_payload_missing_name),
            content_type='application/json',
            headers={'Authorization': f"Token {self.token.data['token']}"}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Nome do serviço é um campo obrigatório')
        
    def test_edit_service_nonexistent_id(self):
        response = self.client.put(
            self.edit_service_url,
            data=json.dumps(self.invalid_payload_nonexistent_id),
            content_type='application/json',
            headers={'Authorization': f"Token {self.token.data['token']}"}
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn(response.data, 'Serviço não encontrado')

    def test_edit_service_wrong_token(self):
        response = self.client.put(
            self.edit_service_url,
            data=json.dumps(self.valid_payload),
            content_type='application/json',
            headers={'Authorization': 'Token 3be1db43f5107736135956946f4a35f1031fba82'}
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['detail'], 'Invalid token.')
        
class CreatePlanTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.create_plan_url = reverse('create_plan')
        self.create_url = reverse('create')
        self.create_service_url = reverse('create_service')
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
        self.service_one = {
            'name': 'Test Service',
            'description': 'Test Description'
        }
        self.service_two = {
            'name': 'Test Service 2',
            'description': 'Test Description'
        }
        self.valid_payload = {
            'name': 'Test Plan',
            'description': 'Test Description',
            'services': [
                {
                    'id': 1,
                    'price': 100.0,
                    'quantity': 2,
                    'description': 'Service Description'
                },
                {
                    'id': 2,
                    'price': 300.0,
                    'quantity': 2,
                    'description': 'Service Description'
                }
            ]
        }
        self.invalid_payload_missing_name = {
            'description': 'Test Description',
            'services': [
                {
                    'id': 1,
                    'price': 100.0,
                    'quantity': 2,
                    'description': 'Service Description'
                }
            ]
        }
        self.invalid_payload_missing_services = {
            'name': 'Test Plan',
            'description': 'Test Description'
        }
        self.invalid_payload_existing_name = {
            'name': 'Test Plan',
            'description': 'Another Description',
            'services': [
                {
                    'id': 1,
                    'price': 100.0,
                    'quantity': 2,
                    'description': 'Service Description'
                }
            ]
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
        
        self.client.post(
            self.create_service_url,
            data=json.dumps(self.service_one),
            content_type='application/json',
            headers={'Authorization': f"Token {self.token.data['token']}"}
        )
        
        self.client.post(
            self.create_service_url,
            data=json.dumps(self.service_two),
            content_type='application/json',
            headers={'Authorization': f"Token {self.token.data['token']}"}
        )

    def test_create_plan_success(self):
        response = self.client.post(
            self.create_plan_url,
            data=json.dumps(self.valid_payload),
            content_type='application/json',
            headers={'Authorization': f"Token {self.token.data['token']}"}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, 'Plano cadastrado com sucesso')

    def test_create_plan_missing_name(self):
        response = self.client.post(
            self.create_plan_url,
            data=json.dumps(self.invalid_payload_missing_name),
            content_type='application/json',
            headers={'Authorization': f"Token {self.token.data['token']}"}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Nome do plano é obrigatório')

    def test_create_plan_missing_services(self):
        response = self.client.post(
            self.create_plan_url,
            data=json.dumps(self.invalid_payload_missing_services),
            content_type='application/json',
            headers={'Authorization': f"Token {self.token.data['token']}"}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Serviços são obrigatórios')

    def test_create_plan_existing_name(self):
        self.client.post(
            self.create_plan_url,
            data=json.dumps(self.valid_payload),
            content_type='application/json',
            headers={'Authorization': f"Token {self.token.data['token']}"}
        )
        response = self.client.post(
            self.create_plan_url,
            data=json.dumps(self.invalid_payload_existing_name),
            content_type='application/json',
            headers={'Authorization': f"Token {self.token.data['token']}"}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Plano com nome existente')

    def test_create_plan_wrong_token(self):
        response = self.client.post(
            self.create_plan_url,
            data=json.dumps(self.valid_payload),
            content_type='application/json',
            headers={'Authorization': 'Token 3be1db43f5107736135956946f4a35f1031fba82'}
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['detail'], 'Invalid token.')
        
class GetAllPlansTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.get_all_plans_url = reverse('get_all_plans')
        self.create_url = reverse('create')
        self.create_service_url = reverse('create_service')
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
        self.service_one = {
            'name': 'Test Service',
            'description': 'Test Description'
        }
        self.service_two = {
            'name': 'Test Service 2',
            'description': 'Test Description'
        }
        self.valid_payload = {
            'name': 'Test Plan',
            'description': 'Test Description',
            'services': [
                {
                    'id': 1,
                    'price': 100.0,
                    'quantity': 2,
                    'description': 'Service Description'
                },
                {
                    'id': 2,
                    'price': 300.0,
                    'quantity': 2,
                    'description': 'Service Description'
                }
            ]
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
        self.client.post(
            self.create_service_url,
            data=json.dumps(self.service_one),
            content_type='application/json',
            headers={'Authorization': f"Token {self.token.data['token']}"}
        )
        self.client.post(
            self.create_service_url,
            data=json.dumps(self.service_two),
            content_type='application/json',
            headers={'Authorization': f"Token {self.token.data['token']}"}
        )
        self.client.post(
            reverse('create_plan'),
            data=json.dumps(self.valid_payload),
            content_type='application/json',
            headers={'Authorization': f"Token {self.token.data['token']}"}
        )

    def test_get_all_plans_success(self):
        response = self.client.get(
            self.get_all_plans_url,
            content_type='application/json',
            headers={'Authorization': f"Token {self.token.data['token']}"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertEqual(len(response.data), 1)

    def test_get_all_plans_no_authentication(self):
        response = self.client.get(
            self.get_all_plans_url,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
class EditPlanTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.create_plan_url = reverse('create_plan')
        self.edit_plan_url = reverse('edit_plan')
        self.create_url = reverse('create')
        self.create_service_url = reverse('create_service')
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
        self.service_one = {
            'name': 'Test Service',
            'description': 'Test Description'
        }
        self.service_two = {
            'name': 'Test Service 2',
            'description': 'Test Description'
        }
        self.plan = {
            'name': 'Test Plan',
            'description': 'Test Description',
            'services': [
                {
                    'id': 1,
                    'price': 100.0,
                    'quantity': 2,
                    'description': 'Service Description'
                },
                {
                    'id': 2,
                    'price': 300.0,
                    'quantity': 2,
                    'description': 'Service Description'
                }
            ]
        }
        self.valid_payload = {
            'id': 1,
            'name': 'Updated Plan',
            'description': 'Updated Description'
        }
        self.invalid_payload_missing_id = {
            'name': 'Updated Plan',
            'description': 'Updated Description'
        }
        self.invalid_payload_missing_name = {
            'id': 1,
            'description': 'Updated Description'
        }
        self.invalid_payload_nonexistent_id = {
            'id': 999,
            'name': 'Nonexistent Plan',
            'description': 'Nonexistent Description'
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
        
        self.client.post(
            self.create_service_url,
            data=json.dumps(self.service_one),
            content_type='application/json',
            headers={'Authorization': f"Token {self.token.data['token']}"}
        )
        
        self.client.post(
            self.create_service_url,
            data=json.dumps(self.service_two),
            content_type='application/json',
            headers={'Authorization': f"Token {self.token.data['token']}"}
        )
        
        self.client.post(
            self.create_plan_url,
            data=json.dumps(self.plan),
            content_type='application/json',
            headers={'Authorization': f"Token {self.token.data['token']}"}
        )

    def test_edit_plan_success(self):
        response = self.client.put(
            self.edit_plan_url,
            data=json.dumps(self.valid_payload),
            content_type='application/json',
            headers={'Authorization': f"Token {self.token.data['token']}"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, 'Plano alterado com sucesso')
        
    def test_edit_plan_missing_id(self):
        response = self.client.put(
            self.edit_plan_url,
            data=json.dumps(self.invalid_payload_missing_id),
            content_type='application/json',
            headers={'Authorization': f"Token {self.token.data['token']}"}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'ID do plano é um campo obrigatório')

    def test_edit_plan_missing_name(self):
        response = self.client.put(
            self.edit_plan_url,
            data=json.dumps(self.invalid_payload_missing_name),
            content_type='application/json',
            headers={'Authorization': f"Token {self.token.data['token']}"}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Nome do plano é um campo obrigatório')

    def test_edit_plan_nonexistent_id(self):
        response = self.client.put(
            self.edit_plan_url,
            data=json.dumps(self.invalid_payload_nonexistent_id),
            content_type='application/json',
            headers={'Authorization': f"Token {self.token.data['token']}"}
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], 'Plano não encontrado')

    def test_edit_plan_wrong_token(self):
        response = self.client.put(
            self.edit_plan_url,
            data=json.dumps(self.valid_payload),
            content_type='application/json',
            headers={'Authorization': 'Token 3be1db43f5107736135956946f4a35f1031fba82'}
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['detail'], 'Invalid token.')

class GetAllPlanServicesTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.get_all_plan_services_url = reverse('get_all_plan_services')
        self.create_url = reverse('create')
        self.create_service_url = reverse('create_service')
        self.create_plan_url = reverse('create_plan')
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
        self.service_one = {
            'name': 'Test Service',
            'description': 'Test Description'
        }
        self.service_two = {
            'name': 'Test Service 2',
            'description': 'Test Description'
        }
        self.plan = {
            'name': 'Test Plan',
            'description': 'Test Description',
            'services': [
                {
                    'id': 1,
                    'price': 100.0,
                    'quantity': 2,
                    'description': 'Service Description'
                },
                {
                    'id': 2,
                    'price': 300.0,
                    'quantity': 2,
                    'description': 'Service Description'
                }
            ]
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
        
        self.client.post(
            self.create_service_url,
            data=json.dumps(self.service_one),
            content_type='application/json',
            headers={'Authorization': f"Token {self.token.data['token']}"}
        )
        
        self.client.post(
            self.create_service_url,
            data=json.dumps(self.service_two),
            content_type='application/json',
            headers={'Authorization': f"Token {self.token.data['token']}"}
        )
        
        self.client.post(
            self.create_plan_url,
            data=json.dumps(self.plan),
            content_type='application/json',
            headers={'Authorization': f"Token {self.token.data['token']}"}
        )

    def test_get_all_plan_services_success(self):
        response = self.client.get(
            self.get_all_plan_services_url,
            {'id': 1},
            content_type='application/json',
            headers={'Authorization': f"Token {self.token.data['token']}"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertEqual(len(response.data), 2)

    def test_get_all_plan_services_nonexistent_plan(self):
        response = self.client.get(
            self.get_all_plan_services_url,
            {'id': 999},
            content_type='application/json',
            headers={'Authorization': f"Token {self.token.data['token']}"}
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], 'Plano não encontrado')

    def test_get_all_plan_services_no_authentication(self):
        response = self.client.get(
            self.get_all_plan_services_url,
            {'id': 1},
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['detail'], 'Authentication credentials were not provided.')

    def test_get_all_plan_services_wrong_token(self):
        response = self.client.get(
            self.get_all_plan_services_url,
            {'id': 1},
            content_type='application/json',
            headers={'Authorization': 'Token 3be1db43f5107736135956946f4a35f1031fba82'}
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['detail'], 'Invalid token.')
        
class AddServiceToPlanTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.add_service_to_plan_url = reverse('add_service_to_plan')
        self.create_url = reverse('create')
        self.create_service_url = reverse('create_service')
        self.create_plan_url = reverse('create_plan')
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
        self.service_one = {
            'name': 'Test Service',
            'description': 'Test Description'
        }
        self.service_two = {
            'name': 'Test Service 2',
            'description': 'Test Description'
        }
        self.plan = {
            'name': 'Test Plan',
            'description': 'Test Description',
            'services': [
                {
                    'id': 1,
                    'price': 100.0,
                    'quantity': 2,
                    'description': 'Service Description'
                },
            ]
        }
        self.valid_payload = {
            'plan_id': 1,
            'service_id': 2,
            'price': 100.0,
            'quantity': 2,
            'description': 'Service Description'
        }
        self.invalid_payload_nonexistent_plan = {
            'plan_id': 999,
            'service_id': 1,
            'price': 100.0,
            'quantity': 2,
            'description': 'Service Description'
        }
        self.invalid_payload_nonexistent_service = {
            'plan_id': 1,
            'service_id': 999,
            'price': 100.0,
            'quantity': 2,
            'description': 'Service Description'
        }
        self.invalid_payload_missing_plan_id = {
            'service_id': 2,
            'price': 200,
            'quantity': 2,
            'description': 'Service Description'
        }
        self.invalid_payload_missing_service_id = {
            'plan_id': 1,
            'price': 300,
            'quantity': 2,
            'description': 'Service Description'
        }
        self.invalid_payload_missing_price = {
            'plan_id': 1,
            'service_id': 2,
            'quantity': 2,
            'description': 'Service Description'
        }
        self.invalid_payload_missing_quantity = {
            'plan_id': 1,
            'service_id': 2,
            'price': 100,
            'description': 'Service Description'
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
        
        self.client.post(
            self.create_service_url,
            data=json.dumps(self.service_one),
            content_type='application/json',
            headers={'Authorization': f"Token {self.token.data['token']}"}
        )
        
        self.client.post(
            self.create_service_url,
            data=json.dumps(self.service_two),
            content_type='application/json',
            headers={'Authorization': f"Token {self.token.data['token']}"}
        )
        
        self.client.post(
            self.create_plan_url,
            data=json.dumps(self.plan),
            content_type='application/json',
            headers={'Authorization': f"Token {self.token.data['token']}"}
        )

    def test_add_service_to_plan_success(self):
        response = self.client.post(
            self.add_service_to_plan_url,
            data=json.dumps(self.valid_payload),
            content_type='application/json',
            headers={'Authorization': f"Token {self.token.data['token']}"}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, 'Serviço adicionado ao plano com sucesso')

    def test_add_service_to_plan_nonexistent_plan(self):
        response = self.client.post(
            self.add_service_to_plan_url,
            data=json.dumps(self.invalid_payload_nonexistent_plan),
            content_type='application/json',
            headers={'Authorization': f"Token {self.token.data['token']}"}
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], 'Plano não encontrado')

    def test_add_service_to_plan_nonexistent_service(self):
        response = self.client.post(
            self.add_service_to_plan_url,
            data=json.dumps(self.invalid_payload_nonexistent_service),
            content_type='application/json',
            headers={'Authorization': f"Token {self.token.data['token']}"}
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], 'Serviço não encontrado')
        
    def test_add_service_to_plan_missing_plan_id(self):
        response = self.client.post(
            self.add_service_to_plan_url,
            data=json.dumps(self.invalid_payload_missing_plan_id),
            content_type='application/json',
            headers={'Authorization': f"Token {self.token.data['token']}"}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'ID do plano é um campo obrigatório')
        
    def test_add_service_to_plan_missing_price(self):
        response = self.client.post(
            self.add_service_to_plan_url,
            data=json.dumps(self.invalid_payload_missing_service_id),
            content_type='application/json',
            headers={'Authorization': f"Token {self.token.data['token']}"}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'ID do serviço é um campo obrigatório')

    def test_add_service_to_plan_missing_price(self):
        response = self.client.post(
            self.add_service_to_plan_url,
            data=json.dumps(self.invalid_payload_missing_price),
            content_type='application/json',
            headers={'Authorization': f"Token {self.token.data['token']}"}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Preço é um campo obrigatório')
        
    def test_add_service_to_plan_missing_quantity(self):
        response = self.client.post(
            self.add_service_to_plan_url,
            data=json.dumps(self.invalid_payload_missing_quantity),
            content_type='application/json',
            headers={'Authorization': f"Token {self.token.data['token']}"}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Quantidade é um campo obrigatório')

    def test_add_service_to_plan_wrong_token(self):
        response = self.client.post(
            self.add_service_to_plan_url,
            data=json.dumps(self.valid_payload),
            content_type='application/json',
            headers={'Authorization': 'Token 3be1db43f5107736135956946f4a35f1031fba82'}
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['detail'], 'Invalid token.')
        
# class EditPlanServiceTestCase(TestCase):
#     def setUp(self):
#         self.client = Client()
#         self.edit_plan_service_url = reverse('edit_plan_service')
#         self.create_url = reverse('create')
#         self.create_service_url = reverse('create_service')
#         self.create_plan_url = reverse('create_plan')
#         self.fake_user = {
#             'name': 'FakeUser',
#             'company_name': 'Fake Company',
#             'email': 'fake@example.com',
#             'password': 'password123',
#             'phone': '12934567890',
#             'cnpj': '12345678901230',
#             'address': '123 Test St',
#             'city': 'Test City',
#             'state': 'Test State',
#             'postalcode': '12345'
#         }
#         self.service_one = {
#             'name': 'Test Service',
#             'description': 'Test Description'
#         }
#         self.plan = {
#             'name': 'Test Plan',
#             'description': 'Test Description',
#             'services': [
#                 {
#                     'id': 1,
#                     'price': 100.0,
#                     'quantity': 2,
#                     'description': 'Service Description'
#                 }
#             ]
#         }
#         self.valid_payload = {
#             'id': 1,
#             'price': 200.0,
#             'quantity': 3,
#             'description': 'Updated Service Description'
#         }
#         self.invalid_payload_nonexistent_id = {
#             'id': 999,
#             'price': 200.0,
#             'quantity': 3,
#             'description': 'Updated Service Description'
#         }
#         self.invalid_payload_missing_id = {
#             'quantity': 3,
#             'description': 'Updated Service Description'
#         }
#         self.client.post(
#             self.create_url,
#             data=json.dumps(self.fake_user),
#             content_type='application/json'
#         )
        
#         self.token_url = reverse('token')
#         self.token = self.client.post(
#             self.token_url,
#             data=json.dumps({'email': 'fake@example.com', 'password': 'password123'}),
#             content_type='application/json'
#         )
        
#         self.client.post(
#             self.create_service_url,
#             data=json.dumps(self.service_one),
#             content_type='application/json',
#             headers={'Authorization': f"Token {self.token.data['token']}"}
#         )
        
#         self.client.post(
#             self.create_plan_url,
#             data=json.dumps(self.plan),
#             content_type='application/json',
#             headers={'Authorization': f"Token {self.token.data['token']}"}
#         )

#     def test_edit_plan_service_success(self):
#         response = self.client.put(
#             self.edit_plan_service_url,
#             data=json.dumps(self.valid_payload),
#             content_type='application/json',
#             headers={'Authorization': f"Token {self.token.data['token']}"}
#         )
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data, 'Serviço do plano alterado com sucesso')

#     def test_edit_plan_service_nonexistent_id(self):
#         response = self.client.put(
#             self.edit_plan_service_url,
#             data=json.dumps(self.invalid_payload_nonexistent_id),
#             content_type='application/json',
#             headers={'Authorization': f"Token {self.token.data['token']}"}
#         )
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
#         self.assertEqual(response.data['error'], 'Serviço do plano não encontrado')

#     def test_edit_plan_service_missing_id(self):
#         response = self.client.put(
#             self.edit_plan_service_url,
#             data=json.dumps(self.invalid_payload_missing_id),
#             content_type='application/json',
#             headers={'Authorization': f"Token {self.token.data['token']}"}
#         )
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertEqual(response.data['error'], 'ID do serviço é um campo obrigatório')

#     def test_edit_plan_service_wrong_token(self):
#         response = self.client.put(
#             self.edit_plan_service_url,
#             data=json.dumps(self.valid_payload),
#             content_type='application/json',
#             headers={'Authorization': 'Token 3be1db43f5107736135956946f4a35f1031fba82'}
#         )
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
#         self.assertEqual(response.data['detail'], 'Invalid token.')




