#!/usr/bin/env python 
from unittest import TestCase
import json

from .deliver_loyalty_accrual import DeliverLoyaltyTransaction

class CalculateLoyaltyTransactionTestCase(TestCase):

    def setUp(self):
        self.api_user = 'microservice'
        self.api_pass = 'microservice'
        
        self.qtp = DeliverLoyaltyTransaction('localhost','super','super')
        self.accrual = json.loads('{"type":"LoyaltyTransaction","url":"https://cbe.sphinx.co.nz/api/loyalty/loyalty_transaction/1/","created":"2017-09-11T04:46:33.224122Z","scheme":{"type":"LoyaltyScheme","url":"https://cbe.sphinx.co.nz/api/loyalty/loyalty_scheme/1/","name":"Airpoints"},"vendor":"https://cbe.sphinx.co.nz/api/party/organisation/1/","promotion":null,"sale":"https://cbe.sphinx.co.nz/api/sale/sale/1/","items":[],"loyalty_amount":"0.10","identification":{"type":"Identification","url":"https://cbe.sphinx.co.nz/api/human_resources/identification/1/","identification_type":"https://cbe.sphinx.co.nz/api/human_resources/identification_type/Airpoints%20Card/","number":"1234567","pin":null,"party":{"type":"Individual","url":"https://cbe.sphinx.co.nz/api/party/individual/1/","user":null,"name":"Unknown","given_names":"","family_names":"","middle_names":"","form_of_address":"","gender":null,"legal_name":"","marital_status":null,"nationality":null,"place_of_birth":"","identifications":["https://cbe.sphinx.co.nz/api/human_resources/identification/1/"]}}}')

        
    def test_accrual(self):
        """
        Test delivery of loyalty accrual
        """
        
        self.qtp.worker(self.accrual)

        
