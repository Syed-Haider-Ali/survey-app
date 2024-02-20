import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from user_auth.models import User
from .data import user_obj



@pytest.mark.django_db
class TestRegister:
    def setup_method(self):
        self.client = APIClient()
        self.url = reverse('register')

    def test_register_success(self):
        print('\n\ntest_register_success')
        print('url:',self.url)
        data = {
            "first_name": "haider",
            "email": "haider@gmail.com",
            "username": "haider@gmail.com",
            "password": "admin1234",
        }
        print('payload: ',data)
        response = self.client.post(self.url, data)
        print('response: ',response.json())
        assert response.status_code == status.HTTP_200_OK

    def test_register_fail(self):
        print('\ntest_register_fail')
        print('url:',self.url)
        data = {
            "first_name": "haider",
            "email": "haider@gmail.com",
            "username": "haider@gmail.com",
            "password": "admin",
        }
        print('payload: ',data)
        response = self.client.post(self.url, data)
        print('response: ',response.json())
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestLogin:
    def setup_method(self):
        self.user = User.objects.create(**user_obj())
        self.client = APIClient()
        self.url = reverse('login')

    def test_login_success(self):
        print('\ntest_login_success')
        print('url:',self.url)
        data = {
            "email": "haider@gmail.com",
            "password": "admin1234"
        }
        print('payload: ',data)
        response = self.client.post(self.url, data)
        print(response.json())
        assert response.status_code == status.HTTP_200_OK

    def test_login_fail_wrong_password(self):
        print('\ntest_login_fail_wrong_password')
        print('url:',self.url)
        data = {
            "email": "haider@gmail.com",
            "password": "admin123487384384378"
        }
        print('payload: ',data)
        response = self.client.post(self.url, data)
        print('response:',response.json())
        assert response.status_code == status.HTTP_400_BAD_REQUEST

