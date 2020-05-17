from django.urls import reverse
from test_plus.test import TestCase


class TestUserAuthenticationAPI(TestCase):

    def setUp(self):
        self.data = {
            'email': 'test@gmail.com',
            'password': 'password',
            'password2': 'password',
            'username': 'test'
        }

    def test_registration(self):
        response = self.client.post(
            path=reverse('account_register'),
            data=self.data,
            format='json')
        self.assertEqual(response.status_code, 201)

        # login
        response = self.client.post(
            path=reverse('account_login'),
            data={
            'username': self.data['username'],
            'password': self.data['password']
            },
            format='json')
        self.assertEqual(response.status_code, 200)

    def test_registration_invalid_data(self):
        # password2 and email is required 
        response = self.client.post(
            path=reverse('account_register'),
            data={
            'username': self.data['username'],
            'password': self.data['password']
            },
            format='json')
        self.assertEqual(response.status_code, 400)


