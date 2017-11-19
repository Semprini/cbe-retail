#!/usr/bin/env python 
import os, sys, json, time
from datetime import datetime, timedelta
import pickle
import logging

from cbe.utils.microservices.queue_trigger_pattern import QueueTriggerPattern, RetryableError, FatalError

from xero import Xero
from xero.auth import PublicCredentials
from local_settings import CREDENTIALS

logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(levelname)s | %(message)s')

NAME = 'transmit_billing_data'    
EXCHANGES = (('notify.retail.sale.Sale.updated',None),('notify.retail.sale.Sale.created',None))


def get_xero_connection(account):
    try:
        with open( "%s_credentials.pickle"%account,'rb' ) as f :
            saved_state = pickle.load(f)
        credentials = PublicCredentials(**saved_state)
        if credentials.expired():
            #credentials.refresh() Partner creds
            raise ValueError('Credentials Expired')
    except( IOError, ValueError ):
        credentials = PublicCredentials(CREDENTIALS['KEY'],CREDENTIALS['SECRET'])
        print( credentials.url )
        token = input('code:')
        credentials.verify(token)

    with open( "%s_credentials.pickle"%account, 'wb' ) as f :
        pickle.dump(credentials.state,f, pickle.HIGHEST_PROTOCOL)
        
    return Xero(credentials)

    
def test_xero():
    xero = get_xero_connection('test')

    data = {
        'Type': 'ACCPAY',
        'Contact': {'Name': 'Test Contact'},
        'Date': datetime.now(),
        'DueDate': datetime.now() + timedelta(days=14),
        'LineAmountTypes': 'Exclusive',
        'LineItems': [
            {'Description': 'Test line item', 'Quantity': 1, 'UnitAmount': 10, 'AccountCode': 200},
        ],
    }
    result = xero.invoices.put(data)
    print( result )

    result = xero.invoices.all()
    print( result )
    
    
class DeliverToXero(QueueTriggerPattern):

    def worker(self, message_json):
        account = message_json['account'].split('/')[-2]

        # TODO: Ignore-non account holder sales
        # TODO: Get bill preferences
        
        lineitems = []
        for item in message_json['sale_items']:
            lineitems.append(
                {
                    'Description': 'Job %s'%item['product']['name'], 
                    'Quantity': float(item['quantity']), 
                    'UnitAmount': float(item['amount']),
                    'AccountCode': 200
                }
            )
        
        data = {
            'Type': 'ACCPAY',
            'Contact': {'Name': 'Test Contact'},
            'Date': datetime.now(),
            'DueDate': datetime.now() + timedelta(days=14),
            'LineAmountTypes': 'Exclusive',
            'LineItems': lineitems, #[ {'Description': 'Test line item', 'Quantity': 1, 'UnitAmount': 10, 'AccountCode': 200}, ],
        }
        xero = get_xero_connection(account)
        result = xero.invoices.put(data)
        print( result )

            
if __name__ == "__main__":
    qtp = DeliverToXero(NAME, EXCHANGES, os.environ['QUEUE_HOST'],os.environ['QUEUE_USER'],os.environ['QUEUE_PASS'])
    qtp.main_loop()
    
