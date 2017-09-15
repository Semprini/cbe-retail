#!/usr/bin/env python 
from unittest import TestCase
import json

from .calculate_loyalty_transaction import CalculateLoyaltyTransaction

class CalculateLoyaltyTransactionTestCase(TestCase):

    def setUp(self):
        self.api_host = 'https://cbe.sphinx.co.nz'
        self.api_user = 'microservice'
        self.api_pass = 'microservice'
        
        self.sale = json.loads('{"type":"Sale","url":"https://cbe.sphinx.co.nz/api/sale/sale/1/","channel":"https://cbe.sphinx.co.nz/api/sale/sales_channel/1/","store":"https://cbe.sphinx.co.nz/api/store/store/1/","vendor":"https://cbe.sphinx.co.nz/api/party/organisation/2/","datetime":"2000-01-01T07:25:00Z","docket_number":"1","total_amount":"9.98","total_amount_excl":"8.68","total_discount":"0.00","total_tax":"1.30","customer":"https://cbe.sphinx.co.nz/api/customer/customer/1234567/","account":"https://cbe.sphinx.co.nz/api/customer/account/1234567/","purchaser":null,"identification":"https://cbe.sphinx.co.nz/api/human_resources/identification/1/","promotion":null,"till":"https://cbe.sphinx.co.nz/api/resource/physical_resource/1/","staff":"https://cbe.sphinx.co.nz/api/human_resources/staff/1/","price_channel":null,"price_calculation":null,"tenders":[{"type":"Tender","url":"https://cbe.sphinx.co.nz/api/sale/tender/1/","sale":"https://cbe.sphinx.co.nz/api/sale/sale/1/","tender_type":{"type":"TenderType","url":"https://cbe.sphinx.co.nz/api/sale/tender_type/1/","valid_from":null,"valid_to":null,"name":"Cash","description":""},"amount":"9.98","reference":null}],"credit_balance_events":[],"sale_items":[{"type":"SaleItem","url":"https://cbe.sphinx.co.nz/api/sale/sale_item/1/","sale":"https://cbe.sphinx.co.nz/api/sale/sale/1/","product_offering":"https://cbe.sphinx.co.nz/api/product/product_offering/243728/","product":{"type":"Product","url":"https://cbe.sphinx.co.nz/api/product/product/1/","code":"243728","name":"GAS CARTRIDGE BUTANE 220G 4 PACK NO. 8","description":"","bundle":[],"categories":[],"cross_sell_products":[],"product_offerings":["https://cbe.sphinx.co.nz/api/product/product_offering/243728/"]},"product_offering_price":"https://cbe.sphinx.co.nz/api/price/product_offering_price/1/","quantity":"1.0000","unit_of_measure":"each","amount":"8.68","discount":"0.00","promotion":null,"cost_price":"6.68"}]}')
        self.payment = json.loads('{"type":"CustomerPayment","url":"https://cbe.sphinx.co.nz/api/accounts_receivable/customer_payment/1/","channel":"https://cbe.sphinx.co.nz/api/accounts_receivable/payment_channel/1/","vendor":"https://cbe.sphinx.co.nz/api/party/organisation/1/","datetime":"2017-09-14T11:23:53Z","docket_number":null,"customer":"https://cbe.sphinx.co.nz/api/customer/customer/ZZBUCKLL/","account":{"type":"CustomerAccount","url":"https://cbe.sphinx.co.nz/api/customer/account/ZZBUCKLL/","created":"2017-09-11","valid_from":null,"valid_to":null,"customer":"https://cbe.sphinx.co.nz/api/customer/customer/ZZBUCKLL/","account_number":"ZZBUCKLL","account_status":"new","managed_by":"https://cbe.sphinx.co.nz/api/party/organisation/1/","credit_liabilities":[],"account_type":"test","name":"test","pin":null,"customer_account_contact":["https://cbe.sphinx.co.nz/api/customer/customer_account_contact/1/"]},"amount":"12.50","tax":"2.50"}')
        
        self.qtp = CalculateLoyaltyTransaction('localhost','super','super')
        

    def test_sale(self):
        """
        Test creation of loyalty transaction from sale
        """
        
        self.qtp.create_loyalty_data_from_sale(self.sale)

        
    def test_payment(self):
        """
        Test creation of loyalty transaction from sale
        """
        
        self.qtp.create_loyalty_data_from_payment(self.payment)      

        