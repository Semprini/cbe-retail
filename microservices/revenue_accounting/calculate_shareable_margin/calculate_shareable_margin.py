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

service_charge_template = '{ "total_margin": "{TOTAL_MARGIN}", "home_margin": "{HOME_MARGIN}", "satellite_margin": "{SATELLITE_MARGIN}", "bill": "{BILL}", "service_bill_item": null, "sales": {SALES}, "home_store": "{HOME_STORE}", "satellite_store": "{SATELLITE_STORE}" }'


class CalculateShareableMargin(QueueTriggerPattern):
    
    def worker(self, message_json):
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
            response = requests.get(sale_url, auth=(API_USER, API_PASS))
            if response.status_code >= 500 or response.status_code in (401,403):
                logging.warning( "Retryable error calculating shareable margin. Could not get sale info:{}".format(response.content) )
                raise RequeableError("Get sale returned: {}".format(response.status_code))
            elif response.status_code != 200:   
                # Fatal errors which can't be retried
                logging.error( "Fatal error calculating shareable margin. Could not get sale info:{}".format(response.content) )
                raise FatalError("Get sale returned: {}".format(response.status_code))
        
            sale = json.loads(response.text)
            satellite_store = sale['vendor']
        
            if home_store == satellite_store:
                logging.info( "Sale is a home store sale, no shareable margin on sale {}".format(sale_url) )
            else:
                total += float(sale['amount'])
                service_charge_sales.append(sale_url)
                
        # Fill out Service charge json
        data = service_charge_template\
            .replace("{BILL}",message_json['url'])\
            .replace('{SALES}',"{}".format(service_charge_sales))\
            .replace('{HOME_STORE}',home_store)\
            .replace('{SATELLITE_STORE}',satellite_store)\
            .replace('{TOTAL_MARGIN}',"{:0.2f}".format(total))\
            .replace('{HOME_MARGIN}',"{:0.2f}".format(total/RATE))\
            .replace('{SATELLITE_MARGIN}',"{:0.2f}".format(total-(total/RATE)))
            
        # Create a new Service charge transaction by calling API
        headers = {'Content-type': 'application/json',}
        response = requests.post(SERVICE_CHARGE_URL, data=data, headers=headers, auth=(API_USER, API_PASS))
        if response.status_code == 201: # (201) Created
            logging.info( "Service charge created" )
        elif response.status_code >= 500 or response.status_code in (401,403):
            logging.warning( "Retryable error creating Service charge: {}".format(response.content) )
            raise RequeableError("Post service charge returned: {}".format(response.status_code))
        else:   
            # Fatal errors which can't be retried
            logging.error( "Fatal error creating Service charge: {}".format(response.content) )
            raise FatalError("Post service charge returned: {}".format(response.status_code))


if __name__ == "__main__":
    API_HOST = os.environ['API_HOST']
    API_USER = os.environ['API_USER']
    API_PASS = os.environ['API_PASS']
    
    qtp = CalculateShareableMargin(NAME, EXCHANGES, os.environ['QUEUE_HOST'],os.environ['QUEUE_USER'],os.environ['QUEUE_PASS'])
    qtp.main_loop()
    