from django.contrib.auth.models import User
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate

class RetailAPITests(APITestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.superuser = User.objects.create_superuser('john', 'john@snow.com', 'johnpassword')
        self.client.login(username='john', password='johnpassword')
        self.client.force_authenticate(user=self.superuser)
        

    def test_get_schema(self):
        """
        Test that we can GET the schema
        """
        response = self.client.get('', format='json')
        self.assertEqual(response.exception, False)
        
