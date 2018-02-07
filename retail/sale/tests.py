from django.contrib.auth.models import User
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate

from cbe.party.models import Individual, Organisation
from cbe.customer.models import Customer

from retail.store.models import Store
from retail.sale.models import SalesChannel, Sale

class SaleAPITests(APITestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.superuser = User.objects.create_superuser('john', 'john@snow.com', 'johnpassword')
        self.client.login(username='john', password='johnpassword')
        self.client.force_authenticate(user=self.superuser)
        
        self.channel = SalesChannel.objects.create(name='Test')
        self.store = Store.objects.create(name='Test', enterprise_id=1)
        self.organisation = Organisation.objects.create(name='Pen Inc.', enterprise_id=1)
        
        self.individual = Individual.objects.create(given_names="John", family_names="Doe")
        self.customer = Customer.objects.create(party=self.individual, customer_number="1", customer_status="new")

        self.sale = Sale.objects.create( channel=self.channel, store=self.store, vendor=self.organisation, customer=self.customer )

    def test_get_sale(self):
        """
        Test that we can GET the sample Sale
        """
        url = '/api/sale/sale/{}/'.format(self.sale.pk)
        response = self.client.get(url, format='json')
        self.assertEqual(response.exception, False)
        
    def test_create_sale(self):
        """
        Ensure we can create a new Customer object.
        """
        url = '/api/sale/sale/'
        data = {
            "channel":"http://127.0.0.1:8000/api/sale/sales_channel/1/",
            "store":"http://127.0.0.1:8000/api/store/store/1/",
            "vendor":"http://127.0.0.1:8000/api/party/organisation/1/",
            "datetime":"2018-02-04T00:40:44.313123Z",
            "total_amount":"0.00",
            "total_amount_excl":"0.00",
            "total_discount":"0.00",
            "total_tax":"0.00",
            "customer":"http://127.0.0.1:8000/api/customer/customer/1/",
            "tenders":[],
            "credit_balance_events":[],
            "sale_items":[]}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)