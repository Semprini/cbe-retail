#!/usr/bin/env python 
import os, sys, json
import requests
import logging

from cbe.utils.microservices.queue_trigger_pattern import QueueTriggerPattern, RetryableError, FatalError

logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(levelname)s | %(message)s')

nal_accrue_template = '{"apnumber": "{APNUMBER}","pointcode": "TEST","txndate": "{DATE}","apdamount": "{AMOUNT}","transactionid": "{ID}","partnerreference": "{REFERENCE}","retailer": "{VENDOR}"}'


class mock_response():
    status_code = 201
    content = "Mock response content"
    
    
def mock_post(url,data,headers,auth):
    print( "Mock post of:{}".format(data) )
    return mock_response()

    
class DeliverLoyaltyTransaction(QueueTriggerPattern):
    def __init__(self, queue_host, queue_user, queue_pass):
        self.name = 'loyalty_transaction_deliver'    
        self.exchanges = (('notify.retail.loyalty.LoyaltyTransaction.updated',None),('notify.retail.loyalty.LoyaltyTransaction.created',None))
        super(DeliverLoyaltyTransaction, self).__init__(self.name, self.exchanges, queue_host, queue_user, queue_pass)
        
        self.api_user = 'microservice'
        self.api_pass = 'microservice'

        self.dest_url = 'https://airnz.com'
        self.dest_user = ''
        self.dest_pass = ''
        
        
    def worker(self, message_json):
        # Call CBE to get more info
        vendor = self.request(message_json['vendor'], self.api_user, self.api_pass, "error sending loyalty accrual. Could not get vendor info")
    
        # Fill out nal_accrue_template json
        data = nal_accrue_template\
            .replace("{APNUMBER}","{}".format(message_json['identification']['number']))\
            .replace('{DATE}',"{}".format(message_json['created']))\
            .replace('{AMOUNT}',"{}".format(message_json['loyalty_amount']))\
            .replace('{ID}',"{}".format(message_json['url'].split('/')[-2]))\
            .replace('{REFERENCE}',"{}".format(message_json['url']))\
            .replace('{VENDOR}',"{}".format(vendor['name']))
            
        headers = {'Content-type': 'application/json',}
        #response = requests.post(self.dest_url, data=data, headers=headers, auth=(self.dest_user, self.dest_pass))
        response = mock_post(self.dest_url, data=data, headers=headers, auth=(self.dest_user, self.dest_pass))
        if response.status_code == 201: # (201) Created
            logging.info( "Loyalty accrual sent" )
        elif response.status_code >= 500 or response.status_code in (401,403):
            logging.warning( "Retryable error sending loyalty accrual:{}".format(response.content) )
            raise RetryableError("AirNZ NAL post returned: {}".format(response.status_code))
        else:   
            # Fatal errors which can't be retried
            logging.error( "Fatal error sending loyalty accrual:{}".format(response.content) )
            raise FatalError("AirNZ NAL post returned: {}".format(response.status_code))

        
if __name__ == "__main__":
    qtp = DeliverLoyaltyTransaction( os.environ['QUEUE_HOST'],os.environ['QUEUE_USER'],os.environ['QUEUE_PASS'])
    qtp.api_user = os.environ['API_USER']
    qtp.api_pass = os.environ['API_PASS']
    qtp.main_loop()
    
