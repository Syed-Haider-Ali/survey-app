from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.core.management import call_command

from .models import User

# class VerifyOtpAPITest(APITestCase):
#     def setUp(self):
#         self.user_data = {
#             "first_name": 'Haider',
#             "email": 's.haider0303@gmail.com',
#             "username": "s.haider0303@gmail.com",
#             "password": "abcd1234",
#             "otp": 123456
#         }
#         self.user = User.objects.create_user(**self.user_data)
#         self.url = reverse('verify_otp')
#
#     def test_verify_otp(self):
#         data = {
#             "otp": 123456,
#             "new_password": "alphabeta",
#             "confirm_password": "alphabeta"
#         }
#         response = self.client.post(self.url, data)
#         self.assertEqual(response.status_code, 200)

#
class ForgetPasswordAPITest(APITestCase):
    def setUp(self):
        self.user_data = {
            "first_name": 'Haider',
            "email": 's.haider0303@gmail.com',
            "username": "s.haider0303@gmail.com",
            "password": "abcd1234"
        }
        self.user = User.objects.create_user(**self.user_data)
        self.url = reverse('forget_password')

    def test_forget_password(self):
        data = {"email": self.user_data['email'] }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)

    def test_forget_password_wrong_credential(self):
        data = {"email": "wrong@gmail.com" }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 404)


class ChangePasswordAPITest(APITestCase):
    def setUp(self):
        self.user_data = {
            "first_name": 'Haider',
            "email": 'haider@gmail.com',
            "username": "haider@gmail.com",
            "password": "abcd1234"
        }
        self.user = User.objects.create_user(**self.user_data)
        self.url = reverse('change_password')

    def test_change_password(self):
        self.client.force_authenticate(user=self.user)
        update_password_data = {
            "old_password": self.user_data['password'],
            "new_password": "alpha12345",
            "confirm_password": "alpha12345"
        }
        response = self.client.post(self.url, update_password_data)
        self.assertEqual(response.status_code, 200)

    def test_change_password_wrong_credentials(self):
        self.client.force_authenticate(user=self.user)
        wrong_old_password = {
            "old_password": "wrong_old_password",
            "new_password": "alpha12345",
            "confirm_password": "alpha12345"
        }
        passwords_must_be_7_chars = {
            "old_password": self.user_data['password'],
            "new_password": "alpha",
            "confirm_password": "alph"
        }
        new_passwords_dont_match = {
            "old_password": self.user_data['password'],
            "new_password": "alpha12345",
            "confirm_password": "alpha1234"
        }
        response_wrong_old_password = self.client.post(self.url, wrong_old_password)
        response_passwords_must_be_7_chars = self.client.post(self.url, passwords_must_be_7_chars)
        response_new_passwords_dont_match = self.client.post(self.url, new_passwords_dont_match)
        self.assertEqual(response_wrong_old_password.status_code, 400)
        self.assertEqual(response_passwords_must_be_7_chars.status_code, 400)
        self.assertEqual(response_new_passwords_dont_match.status_code, 400)


class RegisterAPITest(APITestCase):
    def setUp(self):
        self.url = reverse('register')

    def test_create_user(self):
        user_data = {
            'first_name': 'Ali',
            'email': 's.haider0303@gmail.com',
            'username': 's.haider0303@gmail.com',
            'password': 'qwertyuiop123',
        }
        response = self.client.post(self.url, user_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), 1)

    def test_register_without_email(self):
        data_with_blank_email = {
            'first_name': 'Ali',
            'email': '',
            'username': 's.haider0303@gmail.com',
            'password': 'qwertyuiop123',
        }
        data_with_no_email = {
            'first_name': 'Ali',
            'username': 's.haider0303@gmail.com',
            'password': 'qwertyuiop123',
        }
        response_blank_email = self.client.post(self.url, data_with_blank_email)
        response_no_email = self.client.post(self.url, data_with_no_email)
        self.assertEqual(response_blank_email.status_code, 400)
        self.assertEqual(response_no_email.status_code, 400)

    def test_register_without_username(self):
        data_with_blank_username = {
            'first_name': 'Ali',
            'email': 's.haider0303@gmail.com',
            'username': '',
            'password': 'qwertyuiop123',
        }
        data_with_no_username = {
            'first_name': 'Ali',
            'email': 's.haider0303@gmail.com',
            'password': 'qwertyuiop123',
        }
        response_with_blank_username = self.client.post(self.url, data_with_blank_username)
        response_with_no_username = self.client.post(self.url, data_with_no_username)
        self.assertEqual(response_with_blank_username.status_code, 400)
        self.assertEqual(response_with_no_username.status_code, 400)

    def test_register_without_password(self):
        data_with_password_less_than_7 = {
            'first_name': 'Ali',
            'username': 's.haider0303@gmail.com',
            'email': 's.haider0303@gmail.com',
            'password': 'abcd',
        }
        data_with_blank_password = {
            'first_name': 'Ali',
            'username': 's.haider0303@gmail.com',
            'email': 's.haider0303@gmail.com',
            'password': '',
        }
        data_with_no_password = {
            'first_name': 'Ali',
            'username': 's.haider0303@gmail.com',
            'email': 's.haider0303@gmail.com',
        }
        response_with_password_less_than_7 = self.client.post(self.url, data_with_password_less_than_7)
        response_with_blank_password = self.client.post(self.url, data_with_blank_password)
        response_with_no_password = self.client.post(self.url, data_with_no_password)
        self.assertEqual(response_with_password_less_than_7.status_code, 400)
        self.assertEqual(response_with_blank_password.status_code, 400)
        self.assertEqual(response_with_no_password.status_code, 400)


class LoginAPITest(APITestCase):
    def setUp(self):
        self.user_data = {
            "first_name":"haider",
            "email":"haider@gmail.com",
            "username": "haider@gmail.com",
            "password": "abcd1234"
        }
        self.user = User.objects.create_user(**self.user_data)
        self.url = reverse('login')

    def test_login(self):
        login_data = {
            "username": self.user_data['username'],
            "password": self.user_data['password']
        }
        response = self.client.post(self.url, login_data)
        self.assertEqual(response.status_code, 200)

    def test_login_with_wrong_credentials(self):
        login_data_with_wrong_username = {
            "username": "hello@gmail.com",
            "password": self.user_data['password']
        }
        login_data_with_wrong_password = {
            "username": self.user_data['username'],
            "password": "alphabeta"
        }
        response_with_wrong_username = self.client.post(self.url, login_data_with_wrong_username)
        response_with_wrong_password = self.client.post(self.url, login_data_with_wrong_password)
        self.assertEqual(response_with_wrong_username.status_code, 400)
        self.assertEqual(response_with_wrong_password.status_code, 400)

        
        
