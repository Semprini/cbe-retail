#!/usr/bin/env python 
import os, sys, json
import requests
import logging

from cbe.utils.microservices.queue_trigger_pattern import QueueTriggerPattern, RequeableError, FatalError

logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(levelname)s | %(message)s')

LOYALTY_RATE = 0.01

class CalculateLoyaltyTransaction(QueueTriggerPattern):

    def __init__(self, queue_host, queue_user, queue_pass):
        self.name = 'loyalty_transaction'    
        self.exchanges = (('notify.retail.sale.Sale.updated',None),('notify.retail.sale.Sale.created',None))
        super(CalculateLoyaltyTransaction, self).__init__(self.name, self.exchanges, queue_host, queue_user, queue_pass)
        
        self.api_host = 'https://cbe.sphinx.co.nz'
        self.api_user = 'microservice'
        self.api_pass = 'microservice'


    @property
    def loyalty_transaction_url(self):
        return self.api_host + "/api/loyalty/loyalty_transaction/"

        
    @property
    def loyalty_transaction_template(self):
        return '{ "scheme": "' + self.api_host + '/api/loyalty/loyalty_scheme/1/", "vendor": "{VENDOR}", "promotion": null, "sale": {SALE}, "payment": {PAYMENT}, "items": [], "loyalty_amount": "{AMOUNT}", "identification": "{ID}" }'
    
    
    def create_loyalty_data_from_sale(self, message_json):
        data = None
        
        # If the customer swiped a card then add some airpoints
        if message_json['identification'] != None:
            logging.info( "Sale with Airpoints triggered loyalty calc: {0}".format(message_json['url']) )
            total=float(message_json['total_amount'])
            loyalty_amount = total * LOYALTY_RATE
            
            # Fill out LoyaltyTransaction json
            data = self.loyalty_transaction_template\
                .replace("{VENDOR}","{}".format(message_json['vendor']))\
                .replace("{SALE}",'"{}"'.format(message_json['url']))\
                .replace("{PAYMENT}","null")\
                .replace('{AMOUNT}',"{:0.2f}".format(loyalty_amount))\
                .replace('{ID}',"{}".format(message_json['identification']))        
        else:
            logging.info( "Sale with no Airpoints ID so no loyalty created: {0}".format(message_json['url']) )        
        return data
    
    
    def create_loyalty_data_from_payment(self, message_json):
        data = None

        # Get first customer account contact to find account loyalty earner
        if len(message_json['account']['customer_account_contact']) > 0:
            contact = self.request( message_json['account']['customer_account_contact'][0], self.api_user, self.api_pass, 
                                    "error calculating loyalty accrual. Could not get customer account contact info" )
            if len(contact['party']['identifications']) > 0:
                identification = contact['party']['identifications'][0]

                logging.info( "Payment with Airpoints member as contact triggered loyalty calc: {0}".format(message_json['url']) )
                total=float(message_json['amount'])
                loyalty_amount = total * LOYALTY_RATE

                # Fill out LoyaltyTransaction json
                data = self.loyalty_transaction_template\
                    .replace("{VENDOR}","{}".format(message_json['vendor']))\
                    .replace("{PAYMENT}",'"{}"'.format(message_json['url']))\
                    .replace("{SALE}","null")\
                    .replace('{AMOUNT}',"{:0.2f}".format(loyalty_amount))\
                    .replace('{ID}',"{}".format(identification) )
            else:
                logging.info( "Payment with no Airpoints member as contact so no loyalty created: {0}".format(message_json['url']) )
        else:
            logging.info( "Payment with no account contact so no loyalty created: {0}".format(message_json['url']) )
        
        return data

        
    def worker(self, message_json):
        if message_json['type'] == "Sale":
            data = self.create_loyalty_data_from_sale(message_json)
        elif message_json['type'] == "CustomerPayment":
            data = self.create_loyalty_data_from_payment(message_json)
        else:
            raise FatalError("Unknown input type: {}".format(message_json['type']))

        if data:
            # Create a new LoyaltyTransaction transaction by calling API
            headers = {'Content-type': 'application/json',}
            response = requests.post(self.loyalty_transaction_url, data=data, headers=headers, auth=(self.api_user, self.api_pass))
            if response.status_code == 201: # (201) Created
                logging.info( "Loyalty transaction created" )
            elif response.status_code >= 500 or response.status_code in (401,403):
                logging.warning( "Retryable error creating loyalty transaction:{}".format(response.content) )
                raise RequeableError("Loyalty transaction post returned: {}".format(response.status_code))
            else:   
                # Fatal errors which can't be retried
                logging.error( "Fatal error creating loyalty transaction:{}".format(response.content) )
                raise FatalError("Loyalty transaction post returned: {}".format(response.status_code))

        
if __name__ == "__main__":
    qtp = CalculateLoyaltyTransaction(os.environ['QUEUE_HOST'],os.environ['QUEUE_USER'],os.environ['QUEUE_PASS'])
    qtp.api_host = os.environ['API_HOST']
    qtp.api_user = os.environ['API_USER']
    qtp.api_pass = os.environ['API_PASS']

    qtp.main_loop()
    