#!/usr/bin/env python 
import os, sys, json
import requests
import logging

from cbe.utils.microservices.queue_trigger_pattern import QueueTriggerPattern, RequeableError, FatalError

logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(levelname)s | %(message)s')

API_HOST = "https://cbe.sphinx.co.nz"
API_USER = "microservice"
API_PASS = "microservice"

NAME = 'service_charge'    
EXCHANGES = (('notify.retail.customer_bill.CustomerBill.updated',None),('notify.retail.customer_bill.CustomerBill.created',None))

SERVICE_CHARGE_URL = API_HOST + "/api/customer_bill/service_charge/"
RATE = 0.5

service_charge_template = '{ "total_margin": "{TOTAL_MARGIN}", "home_margin": "{HOME_MARGIN}", "satellite_margin": "{SATELLITE_MARGIN}", "bill": "{BILL}", "service_bill_item": null, "sale": "http://127.0.0.1:8000/api/sale/sale/1/", "home_store": "http://127.0.0.1:8000/api/store/store/1/", "satellite_store": "http://127.0.0.1:8000/api/store/store/2/" }'


class CalculateShareableMargin(QueueTriggerPattern):
    
    def worker(self, message_json):
        total=float(message_json['amount'])
        
        # Fill out Service charge json
        data = service_charge_template\
            .replace("{BILL}","{}".format(message_json['url']))\
            .replace('{TOTAL_MARGIN}',"{:0.2f}".format(total))\
            .replace('{HOME_MARGIN}',"{:0.2f}".format(total/RATE))\
            .replace('{SATELLITE_MARGIN}',"{:0.2f}".format(total-(total/RATE)))
            
        # Create a new Service charge transaction by calling API
        headers = {'Content-type': 'application/json',}
        response = requests.post(SERVICE_CHARGE_URL, data=data, headers=headers, auth=(API_USER, API_PASS))
        if response.status_code == 201: # (201) Created
            logging.info( "Service charge created" )
        elif response.status_code >= 500 or response.status_code in (401,403):
            logging.warning( "Retryable error creating Service charge" )
            logging.info( response.__dict__ )
            raise RequeableError()
        else:   
            # Fatal errors which can't be retried
            logging.error( "Fatal error creating Service charge" )
            logging.info( response.__dict__ )
            raise FatalError()


if __name__ == "__main__":
    API_HOST = os.environ['API_HOST']
    API_USER = os.environ['API_USER']
    API_PASS = os.environ['API_PASS']
    
    qtp = CalculateShareableMargin(NAME, EXCHANGES, os.environ['QUEUE_HOST'],os.environ['QUEUE_USER'],os.environ['QUEUE_PASS'])
    qtp.main_loop()
    