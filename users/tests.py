from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from users.models import User


class UserTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email='test@gmail.com', password='testpass')
        self.client.force_authenticate(user=self.user)

    def test_user_create(self):
        url = reverse('users:create_users')
        data = {
            'email': 'test2@gmail.com',
            'password': 'testpass',
            'country': "testcountry",
            'city': "testcity",
            'phone': '123456789'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_list(self):
        url = reverse('users:list_users')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_detail(self):
        url = reverse('users:detail_users', kwargs={'pk': self.user.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_update(self):
        url = reverse('users:update_users', kwargs={'pk': self.user.pk})
        data = {
            'email': 'updated@gmail.com',
            'country': "updated-country",
            'city': "updated-city",
            'phone': '987654321'
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_delete(self):
        url = reverse('users:delete_users', kwargs={'pk': self.user.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
