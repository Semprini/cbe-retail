#!/usr/bin/env python 
import os, sys, json
import requests
import logging

from cbe.utils.microservices.queue_trigger_pattern import QueueTriggerPattern, RequeableError, FatalError

logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(levelname)s | %(message)s')

NAME = 'loyalty_transaction_deliver'    
EXCHANGES = (('notify.retail.loyalty.LoyaltyTransaction.updated',None),('notify.retail.loyalty.LoyaltyTransaction.created',None))

API_USER = 'microservice'
API_PASS = 'microservice'

DEST_URL = 'https://airnz.com'
DEST_USER = ''
DEST_PASS = ''
nal_accrue_template = '{"apnumber": "{APNUMBER}","pointcode": "TEST","txndate": "{DATE}","apdamount": "{AMOUNT}","transactionid": "{ID}","partnerreference": "{REFERENCE}","retailer": "{VENDOR}"}'


class mock_response():
    status_code = 201
    
def mock_post(url,data,headers,auth):
    print( "Mock post of:{}".format(data) )
    return mock_response()

class DeliverLoyaltyTransaction(QueueTriggerPattern):
    
    def worker(self, message_json):
        # Call CBE to get more info
        response = requests.get(message_json['vendor'], auth=(API_USER, API_PASS))
        if response.status_code >= 500 or response.status_code in (401,403):
            logging.warning( "Retryable error sending loyalty accrual. Could not get vendor info." )
            logging.info( response.__dict__ )
            raise RequeableError("Get vendor returned: %s"%response.status_code)
        elif response.status_code != 200:   
            # Fatal errors which can't be retried
            logging.error( "Fatal error sending loyalty accrual. Could not get vendor info." )
            logging.info( response.__dict__ )
            raise FatalError("Get vendor returned: %s"%response.status_code)
    
        vendor = json.loads(response.body)
    
        # Fill out nal_accrue_template json
        data = nal_accrue_template\
            .replace("{APNUMBER}","{}".format(message_json['identification']['number']))\
            .replace('{DATE}',"{}".format(message_json['created']))\
            .replace('{AMOUNT}',"{}".format(message_json['loyalty_amount']))\
            .replace('{ID}',"{}".format(message_json['url'].split('/')[-2]))\
            .replace('{REFERENCE}',"{}".format(message_json['url']))\
            .replace('{VENDOR}',"{}".format(vendor['name']))
            
        headers = {'Content-type': 'application/json',}
        #response = requests.post(DEST_URL, data=data, headers=headers, auth=(DEST_USER, DEST_PASS))
        response = mock_post(DEST_URL, data=data, headers=headers, auth=(DEST_USER, DEST_PASS))
        if response.status_code == 201: # (201) Created
            logging.info( "Loyalty accrual sent" )
        elif response.status_code >= 500 or response.status_code in (401,403):
            logging.warning( "Retryable error sending loyalty accrual" )
            logging.info( response.__dict__ )
            raise RequeableError("AirNZ NAL post returned: %s"%response.status_code)
        else:   
            # Fatal errors which can't be retried
            logging.error( "Fatal error sending loyalty accrual" )
            logging.info( response.__dict__ )
            raise FatalError("AirNZ NAL post returned: %s"%response.status_code)

        
if __name__ == "__main__":
    API_USER = os.environ['API_USER']
    API_PASS = os.environ['API_PASS']

    qtp = DeliverLoyaltyTransaction(NAME, EXCHANGES, os.environ['QUEUE_HOST'],os.environ['QUEUE_USER'],os.environ['QUEUE_PASS'])
    qtp.main_loop()
    