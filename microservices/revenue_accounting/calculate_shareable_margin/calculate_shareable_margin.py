#!/usr/bin/env python 
import os, sys, json
import requests
import logging

from cbe.utils.microservices.queue_trigger_pattern import QueueTriggerPattern, RetryableError, FatalError

logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(levelname)s | %(message)s')

RATE = 0.5

service_charge_template = '{ "total_margin": "{TOTAL_MARGIN}", "home_margin": "{HOME_MARGIN}", "satellite_margin": "{SATELLITE_MARGIN}", "bill": "{BILL}", "service_bill_item": null, "sales": {SALES}, "home_store": "{HOME_STORE}", "satellite_store": "{SATELLITE_STORE}" }'

class CalculateShareableMargin(QueueTriggerPattern):
    def __init__(self, queue_host, queue_user, queue_pass):
        self.name = 'service_charge'    
        self.exchanges =    (('notify.retail.customer_bill.CustomerBill.updated',None),('notify.retail.customer_bill.CustomerBill.created',None))
                            
        super(CalculateShareableMargin, self).__init__(self.name, self.exchanges, queue_host, queue_user, queue_pass)
        
        self.api_host = 'https://cbe.sphinx.co.nz'
        self.api_user = 'microservice'
        self.api_pass = 'microservice'

        
    @property
    def service_charge_url(self):
        return self.api_host + "/api/customer_bill/service_charge/"
        
        
    def worker(self, message_json, properties):
        total = float(0)
        try:
            sales = message_json['accountbillitems'][0]['sale_events']
        except KeyError:
            print( "No account sales recorded in bill. No service charge to calculate" )
            return
        home_store = message_json['account']['managed_by']
        
        service_charge_sales = []
        
        for sale_url in sales:
            # GET sale to find satellite store
            sale = self.request( sale_url, self.api_user, self.api_pass, 
                                    "error calculating shareable margin. Could not get sale info." )
            
            satellite_store = sale['vendor']
        
            if home_store == satellite_store:
                logging.info( "Sale is a home store sale, no shareable margin on sale {}".format(sale_url) )
            else:
                for item in sale['sale_items']:
                    total += ( float(item['amount']) - float(item['cost_price']) )
                service_charge_sales.append(sale_url)
                
        if total == 0:
            logging.info( "Satellite store sales value is 0, no shareable margin created for bill {}".format(message_json['url']) )
            return
            
        # Fill out Service charge json
        data = service_charge_template\
            .replace("{BILL}",message_json['url'])\
            .replace('{SALES}',json.dumps(service_charge_sales))\
            .replace('{HOME_STORE}',home_store)\
            .replace('{SATELLITE_STORE}',satellite_store)\
            .replace('{TOTAL_MARGIN}',"{:0.2f}".format(total))\
            .replace('{HOME_MARGIN}',"{:0.2f}".format(total*RATE))\
            .replace('{SATELLITE_MARGIN}',"{:0.2f}".format(total-(total*RATE)))
            
        # Create a new Service charge transaction by calling API
        headers = {'Content-type': 'application/json',}
        response = requests.post(self.service_charge_url, data=data, headers=headers, auth=(self.api_user, self.api_pass))
        if response.status_code == 201: # (201) Created
            logging.info( "Service charge created" )
        elif response.status_code >= 500 or response.status_code in (401,403):
            logging.warning( "Retryable error creating Service charge: {}".format(response.content) )
            raise RetryableError("Post service charge returned: {}".format(response.status_code))
        else:   
            # Fatal errors which can't be retried
            logging.error( "Fatal error creating Service charge: {}".format(response.content) )
            raise FatalError("Post service charge returned: {}".format(response.status_code))


if __name__ == "__main__":
    qtp = CalculateShareableMargin(os.environ['QUEUE_HOST'],os.environ['QUEUE_USER'],os.environ['QUEUE_PASS'])
    qtp.api_host = os.environ['API_HOST']
    qtp.api_user = os.environ['API_USER']
    qtp.api_pass = os.environ['API_PASS']
    
    qtp.main_loop()
   
    
