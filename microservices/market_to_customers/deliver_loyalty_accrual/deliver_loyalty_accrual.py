#!/usr/bin/env python 
import os, sys, json
import requests
import logging

from cbe.utils.microservices.queue_trigger_pattern import QueueTriggerPattern, RequeableError, FatalError

logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(levelname)s | %(message)s')

NAME = 'loyalty_transaction_deliver'    
EXCHANGES = (('notify.retail.loyalty.LoyaltyTransaction.updated',None),('notify.retail.loyalty.LoyaltyTransaction.created',None))

API_URL = 'https://airnz.com'
API_USER = ''
API_PASS = ''
nal_accrue_template = '{"apnumber": "{APNUMBER}","pointcode": "TEST","txndate": "{DATE}","apdamount": "{AMOUNT}","transactionid": "{ID}","partnerreference": "{REFERENCE}","retailer": "{VENDOR}"}'


class mock_response():
    status_code = 201
    
def mock_post(url,data,headers,auth):
    return mock_response()

class DeliverLoyaltyTransaction(QueueTriggerPattern):
    
    def worker(self, message_json):

        # Fill out nal_accrue_template json
        data = nal_accrue_template\
            .replace("{APNUMBER}","{}".format(message_json['identification']['number']))\
            .replace('{DATE}',"{}".format(message_json['created']))\
            .replace('{AMOUNT}',"{}".format(message_json['loyalty_amount']))\
            .replace('{ID}',"{}".format(message_json['url'].split('/')[-2]))\
            .replace('{REFERENCE}',"{}".format(message_json['url']))\
            .replace('{VENDOR}',"{}".format(message_json['vendor'].split('/')[-2]))
            
        headers = {'Content-type': 'application/json',}
        #response = requests.post(API_URL, data=data, headers=headers, auth=(API_USER, API_PASS))
        response = mock_post(API_URL, data=data, headers=headers, auth=(API_USER, API_PASS))
        if response.status_code == 201: # (201) Created
            logging.info( "Loyalty accrual sent" )
        elif response.status_code >= 500 or response.status_code in (401,403):
            logging.warning( "Retryable error sending loyalty accrual" )
            logging.info( response.__dict__ )
            raise RequeableError()
        else:   
            # Fatal errors which can't be retried
            logging.error( "Fatal error sending loyalty accrual" )
            logging.info( response.__dict__ )
            raise FatalError()

        
if __name__ == "__main__":
    API_URL = os.environ['API_HOST']
    API_USER = os.environ['API_USER']
    API_PASS = os.environ['API_PASS']
    
    qtp = DeliverLoyaltyTransaction(NAME, EXCHANGES, os.environ['QUEUE_HOST'],os.environ['QUEUE_USER'],os.environ['QUEUE_PASS'])
    qtp.main_loop()
    