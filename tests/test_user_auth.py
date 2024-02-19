import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from user_auth.models import User
from django.contrib.auth.hashers import make_password



@pytest.mark.django_db
class TestRegister:
    def setup_method(self):
        self.client = APIClient()
        self.url = reverse('register')

    def test_register_success(self):
        data = {
            "first_name": "haider",
            "email": "haider@gmail.com",
            "username": "haider@gmail.com",
            "password": "admin1234",
        }
        response = self.client.post(self.url, data)
        assert response.status_code == status.HTTP_200_OK

    def test_register_fail(self):
        data = {
            "first_name": "haider",
            "email": "haider@gmail.com",
            "username": "haider@gmail.com",
            "password": "admin",
        }
        response = self.client.post(self.url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestLogin:
    def setup_method(self):
        user_data = {
            "first_name": "haider",
            "email": "haider@gmail.com",
            "username": "haider@gmail.com",
            "password": make_password("admin1234"),
            "is_active": True,
            "is_locked": False
        }
        self.user = User.objects.create(**user_data)
        self.client = APIClient()
        self.url = reverse('login')

    def test_login_success(self):
        data = {
            "email": "haider@gmail.com",
            "password": "admin1234"
        }
        response = self.client.post(self.url, data)
        assert response.status_code == status.HTTP_200_OK

    def test_login_fail(self):
        data = {
            "email": "haider@gmail.com",
            "password": "admin123487384384378"
        }
        response = self.client.post(self.url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

