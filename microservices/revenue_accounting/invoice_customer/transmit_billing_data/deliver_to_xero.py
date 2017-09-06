#!/usr/bin/env python 
import os, sys, json, time
from datetime import datetime, timedelta
import pickle
import logging

import pika

from xero import Xero
from xero.auth import PublicCredentials
from local_settings import CREDENTIALS

logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(levelname)s | %(message)s')

QUEUE_HOST = "cbemq"
QUEUE_USER = "super"
QUEUE_PASS = "super"

EXCHANGES = ['notify.retail.sale.Sale.updated','notify.retail.sale.Sale.created',]
DLX = 'microservice.transmit_billing_data.dlx'
RETRY_EXCHANGE = 'microservice.transmit_billing_data.retry'
QUEUE = 'microservice.transmit_billing_data.Sale'
RETRY_QUEUE = 'microservice.transmit_billing_data.retry'
RETRY_DELAY = 30000

test_json = '{"type":"Sale","url":"https://cbe.sphinx.co.nz/api/sale/sale/4/","channel":"https://cbe.sphinx.co.nz/api/sale/sales_channel/1/","store":"https://cbe.sphinx.co.nz/api/store/store/1/","seller":"https://cbe.sphinx.co.nz/api/party/organisation/1/","datetime":"2000-01-01T07:41:00Z","docket_number":"4","total_amount":"800.00","total_amount_excl":"695.65","total_discount":"0.00","total_tax":"104.35","customer":"https://cbe.sphinx.co.nz/api/customer/customer/CRMPLUMB/","account":"https://cbe.sphinx.co.nz/api/customer/account/CRMPLUMB/","purchaser":null,"identification":null,"promotion":"https://cbe.sphinx.co.nz/api/price/promotion/1/","till":"https://cbe.sphinx.co.nz/api/resource/physical_resource/1/","staff":"https://cbe.sphinx.co.nz/api/human_resources/staff/2/","price_channel":null,"price_calculation":null,"tenders":[],"credit_balance_events":[{"type":"CreditBalanceEvent","url":"https://cbe.sphinx.co.nz/api/credit/credit_balance_event/1/","credit":"https://cbe.sphinx.co.nz/api/credit/credit/1/","customer":"https://cbe.sphinx.co.nz/api/customer/customer/CRMPLUMB/","account":"https://cbe.sphinx.co.nz/api/customer/account/CRMPLUMB/","datetime":"2017-09-01T00:52:15.437897Z","amount":"800.00","balance":"800.00"}],"sale_items":[{"type":"SaleItem","url":"https://cbe.sphinx.co.nz/api/sale/sale_item/5/","sale":"https://cbe.sphinx.co.nz/api/sale/sale/4/","product_offering":{"type":"ProductOffering","url":"https://cbe.sphinx.co.nz/api/product/product_offering/5/","valid_from":null,"valid_to":null,"product":{"type":"Product","url":"https://cbe.sphinx.co.nz/api/product/product/5/","valid_from":null,"valid_to":null,"name":"NAILER IMPULSE FRAMEMASTER-LI PASLODE","description":"","unit_of_measure":"each","sku":"180837","barcode":null,"bundle":[],"categories":[],"cross_sell_products":[]},"channels":["https://cbe.sphinx.co.nz/api/sale/sales_channel/1/"],"segments":[],"strategies":[],"supplier_code":null,"retail_price":"800.00","product_offering_prices":["https://cbe.sphinx.co.nz/api/price/product_offering_price/5/"],"supplier":null,"buyer":null},"amount":"695.65","discount":"0.00","promotion":"https://cbe.sphinx.co.nz/api/price/promotion/1/"}]}'

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

    
def queue_callback(ch, method, properties, body):
    # Create a disctionary from message body
    message_json=json.loads(body.decode('utf-8'))
    account = message_json['account'].split('/')[-2]

    lineitems = []
    for item in message_json['sale_items']:
        lineitems.append(
            {
                'Description': 'Job %s'%item['product']['name'], 
                'Quantity': 1, 
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

    # TODO: Handle failures with retry or exceptions
    
    # Always ack (after work has completed) as retry handled via new message passed to retry exchange
    logging.info( "ackd:",channel.basic_ack(delivery_tag=method.delivery_tag, multiple=False))
    
    
def test_callback():
    queue_callback(None, None, pika.BasicProperties(headers = {'foo':'a'}), test_json)

    
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
    
    
def queue_setup(connection, callback):
    channel = connection.channel()
    channel.confirm_delivery()

    # Create a queue for our messages to be read from
    result = channel.queue_declare(exclusive=False, queue=QUEUE, durable=True )
    if not result:
        logging.critical( 'Queue didnt declare properly!' )
        sys.exit(1)

    # Subscribe (bind) to object message exchanges
    for exchange in EXCHANGES:
        channel.exchange_declare(exchange=exchange, exchange_type='headers')
        channel.queue_bind(exchange=exchange, queue=QUEUE, routing_key = '',)
                       #arguments = {'ham': 'good', 'x-match':'any'})

    # Create a dead letter exhange where messages from retry queue will be put after TTL
    # Subscribe (bind) our main queue to it for redelivery
    channel.exchange_declare(exchange=DLX, exchange_type='direct')
    channel.queue_bind(exchange=DLX, queue=QUEUE, routing_key = '',)
    
    # Create a retry exchange and queue where messages are held for TTL.
    channel.exchange_declare(exchange=RETRY_EXCHANGE, exchange_type='direct')
    channel.queue_declare(exclusive=False, queue=RETRY_QUEUE, durable=True, arguments={'x-dead-letter-exchange':DLX,'x-message-ttl':RETRY_DELAY} )
    channel.queue_bind(exchange=RETRY_EXCHANGE, queue=RETRY_QUEUE, routing_key = '',)
                       
    channel.basic_consume(callback, queue=QUEUE, no_ack=False)
    return channel
    

def main(host,user,password):
    credentials = pika.PlainCredentials(user, password)
    connection = None
    ready = False
    done = False
    
    while not done:
        while not ready:
            try:
                connection = pika.BlockingConnection(pika.ConnectionParameters(host=host, credentials=credentials))
                logging.info( "Completed connection to MQ..." )
                ready = True
            except KeyboardInterrupt:
                ready = True
                done = True
            except:
                logging.warning( "Connection to MQ not ready, retry..." )
                time.sleep(5)
        try:
           channel = queue_setup(connection, queue_callback)
           channel.start_consuming()
        except pika.exceptions.ConnectionClosed:
            logging.warning( "Connection to MQ closed. retry..." )
            connection = None
            ready = False
            time.sleep(5)
        except KeyboardInterrupt:
            print( 'Bye' )
            done = True
            channel.stop_consuming()

    if connection:
        connection.close()

            
if __name__ == "__main__":
    #test handler:
    #queue_callback(None, None, pika.BasicProperties(headers = {'foo':'a'}), test_json)
    
    main(os.environ['QUEUE_HOST'],os.environ['QUEUE_USER'],os.environ['QUEUE_PASS'])
    