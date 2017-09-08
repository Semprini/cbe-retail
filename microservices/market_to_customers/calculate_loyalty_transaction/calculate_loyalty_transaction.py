#!/usr/bin/env python 
import os, sys, time, json
import requests
import logging

import pika

from cbe.utils.microservices.queue_trigger_pattern import QueueTriggerPattern, RequeableError, FatalError

logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(levelname)s | %(message)s')

API_HOST = "https://cbe.sphinx.co.nz"
API_USER = "microservice"
API_PASS = "microservice"

NAME = 'loyalty_transaction'    
EXCHANGES = (('notify.retail.sale.Sale.updated',None),('notify.retail.sale.Sale.created',None))

LOYALTY_TRANSACTION_URL = API_HOST + "/api/loyalty/loyalty_transaction/"
LOYALTY_RATE = 0.01

loyalty_transaction_template = '{"scheme": "https://cbe.sphinx.co.nz/api/loyalty/loyalty_scheme/1/","promotion": null,"sale": "{SALE}","items": [],"loyalty_amount": {AMOUNT},"identification": "{ID}"}'


class CalculateLoyaltyTransaction(QueueTriggerPattern):
    
    def worker(self, message_json):
        print( "Should override worker and do something here" )

    # If the customer swiped a card then add some airpoints
    if message_json['identification'] != None:
        logging.info( "Sale with Airpoints triggered loyalty calc: {0}".format(message_json['identification']) )
        total=float(message_json['total_amount'])
        loyalty_amount = total * LOYALTY_RATE
        
        # Fill out LoyaltyTransaction json
        data = loyalty_transaction_template\
            .replace("{SALE}","{}".format(message_json['url']))\
            .replace('{AMOUNT}',"{:0.2f}".format(loyalty_amount))\
            .replace('{ID}',"{}".format(message_json['identification']))
            
        # Create a new LoyaltyTransaction transaction by calling API
        headers = {'Content-type': 'application/json',}
        response = requests.post(LOYALTY_TRANSACTION_URL, data=data, headers=headers, auth=(API_USER, API_PASS))
        if response.status_code == 201: # (201) Created
            logging.info( "Loyalty transaction created" )
        elif response.status_code >= 500 or response.status_code in (401,403):
            logging.warning( "Retryable error creating loyalty transaction" )
            logging.info( response.__dict__ )
            raise RequeableError()
        else:   
            # Fatal errors which can't be retried
            logging.error( "Fatal error creating loyalty transaction" )
            logging.info( response.__dict__ )
            raise FatalError()

        
if __name__ == "__main__":
    #test handler:
    #queue_callback(None, None, pika.BasicProperties(headers = {'foo':'a'}), test_json)
    API_HOST = os.environ['API_HOST']
    API_USER = os.environ['API_USER']
    API_PASS = os.environ['API_PASS']
    
    qtp = CalculateLoyaltyTransaction(NAME, EXCHANGES, os.environ['QUEUE_HOST'],os.environ['QUEUE_USER'],os.environ['QUEUE_PASS'])
    qtp.main_loop()
    