from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from utils.tests import JWTLoginBaseTest

User = get_user_model()


class UserRegisterViewTest(APITestCase):
    def setUp(self):
        self.registration_url = reverse('accounts:register')

    def test_register_user(self):
        user_data = dict(
            username='mohammad', phone_number='09121111111', password='QWEasd9876', confirm_password='QWEasd9876'
        )
        response = self.client.post(self.registration_url, data=user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], user_data['username'])
        self.assertEqual(response.data['phone_number'], user_data['phone_number'])
        self.assertTrue('access_token' in response.data)
        self.assertTrue('refresh_token' in response.data)

    def test_duplicate_username(self):
        user_data = dict(
            username='mohammad2', phone_number='09121111111', password='QWEasd9876', confirm_password='QWEasd9876'
        )
        response = self.client.post(self.registration_url, data=user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.post(self.registration_url, data=user_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_user_weak_password(self):
        week_password_user_data = dict(
            username='mohammad', phone_number='09121111111', password='1234', confirm_password='1234'
        )
        response = self.client.post(self.registration_url, data=week_password_user_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_user_not_equal_password(self):
        password_not_equal_user_data = dict(
            username='mohammad', phone_number='09121111111', password='QWEasd9876', confirm_password='QWEasd9874'
        )
        response = self.client.post(self.registration_url, data=password_not_equal_user_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserInfoViewTest(JWTLoginBaseTest):

    def test_get_user_info(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        user_info_url = reverse('accounts:user-info')
        response = self.client.get(user_info_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.user_data['username'])
        self.assertEqual(response.data['phone_number'], self.user_data['phone_number'])


class UserChangePasswordTest(JWTLoginBaseTest):

    def test_change_password(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        user_change_password_url = reverse('accounts:change-password')
        data = {
            'old_password': 'QWEasd9876',
            'new_password': 'Salam0011',
            'confirm_password': 'Salam0011',
        }
        response = self.client.put(user_change_password_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user = User.objects.get(username=self.user_data['username'])
        self.assertTrue(user.check_password('Salam0011'))
