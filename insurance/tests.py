from django.urls import reverse
from rest_framework import status

from insurance.models import Branch
from utils.tests import JWTLoginBaseTest


class LifeInsurance(JWTLoginBaseTest):
    def setUp(self):
        super().setUp()
        self.life_insurance_url = reverse('insurance:life-insurance')
        self.branch = Branch.objects.create(code='111111', name='Tehranpars')

    def test_life_insurance(self):
        data = {
            'first_name': 'amir', 'last_name': 'bonakdar', 'phone_number': '09121111111', 'email': 'admin@admin.com',
            'age': 15, 'bmi': 7.5, 'cigarette': True, 'hookah': True, 'cigarette_number': 12, 'hookah_number': 2,
            'branch': self.branch.pk
        }
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.client.post(self.life_insurance_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_life_insurance_wrong_age(self):
        data = {
            'first_name': 'amir', 'last_name': 'bonakdar', 'phone_number': '09121111111', 'email': 'admin@admin.com',
            'age': 55, 'bmi': 7.5, 'cigarette': True, 'hookah': True, 'cigarette_number': 12, 'hookah_number': 2,
            'branch': self.branch.pk
        }
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.client.post(self.life_insurance_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue('age' in response.data)
