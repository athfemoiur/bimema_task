from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase

User = get_user_model()


class JWTLoginBaseTest(APITestCase):
    def setUp(self):
        self.user_data = dict(
            username='mohammad', phone_number='09121111111', password='QWEasd9876', confirm_password='QWEasd9876'
        )
        User.objects.create_user(username=self.user_data['username'], phone_number=self.user_data['phone_number'],
                                 password=self.user_data['password'])

        token_url = reverse('accounts:token_obtain_pair')
        user_login_data = {'username': self.user_data['username'], 'password': self.user_data['password']}
        self.access_token = self.client.post(token_url, data=user_login_data).data['access']
