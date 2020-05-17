from django.urls import reverse
from test_plus.test import TestCase
import random
import string
from .models import UserAccount, Transaction
from django.contrib.auth.models import User
import json

class TestUserAccountCreateAPI(TestCase):

    def setUp(self):
        self.data = {
            'email': 'test@gmail.com',
            'password': 'password',
            'password2': 'password',
            'username': 'test1'
        }

    def test_create_account(self):
        token = self.login_as_customer()
        response = self.client.post(
            path=reverse('account_create'),
            data=json.dumps({
                "name": "tony"
            }),
            content_type='application/json',
            HTTP_AUTHORIZATION=token)
        self.assertEqual(response.status_code, 201)

    def login_as_customer(self):
        response = self.client.post(
            path=reverse('account_register'),
            data=self.data,
            format='json')
        self.assertEqual(response.status_code, 201)
        return 'Bearer ' + response.data['access']
    
