#!/usr/bin/env python 
import os, sys, time, json
import requests
import logging

import pika

logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(levelname)s | %(message)s')

QUEUE_HOST = "cbemq"
QUEUE_USER = "super"
QUEUE_PASS = "super"

EXCHANGES = ['notify.retail.customer_bill.CustomerBill.updated','notify.retail.customer_bill.CustomerBill.created',]
DLX = 'microservice.service_charge.dlx'
RETRY_EXCHANGE = 'microservice.service_charge.retry'
QUEUE = 'microservice.service_charge.CustomerBill'
RETRY_QUEUE = 'microservice.service_charge.retry'
RETRY_DELAY = 30000

API_HOST = "https://cbe.sphinx.co.nz"
API_USER = "microservice"
API_PASS = "microservice"

SERVICE_CHARGE_URL = API_HOST + "/api/customer_bill/service_charge/"
RATE = 0.5

test_json = '{{ "type": "CustomerBill", "url": "{0}/api/customer_bill/customer_bill/1/",     "number": "1",     "created": "2017-08-24T21:43:42.312476Z",     "period_from": "2017-08-24",     "period_to": "2017-08-24",     "status": "active",     "amount": "0.00",     "discounted": "0.00",     "adjusted": "0.00",     "rebated": "0.00",     "disputed": "0.00",     "allocated": "0.00",     "account": {{ "type": "CustomerAccount", "url": "{0}/api/customer/account/ZZBUCKLL/", "created": "2017-08-24", "valid_from": null, "valid_to": null, "customer": "{0}/api/customer/customer/ZZBUCKLL/", "account_number": "ZZBUCKLL",         "account_status": "new",         "managed_by": "{0}/api/party/organisation/1/",         "credit_liabilities": [],         "account_type": "",         "name": "",         "pin": null,         "customer_account_contact": []     }},     "specification": "{0}/api/customer_bill/customer_bill_specification/1/",     "accountbillitems": [],     "jobbillitems": [] }}'.format(API_HOST)
service_charge_template = '{ "total_margin": "{TOTAL_MARGIN}", "home_margin": "{HOME_MARGIN}", "satellite_margin": "{SATELLITE_MARGIN}", "bill": "{BILL}", "service_bill_item": null, "sale": "http://127.0.0.1:8000/api/sale/sale/1/", "home_store": "http://127.0.0.1:8000/api/store/store/1/", "satellite_store": "http://127.0.0.1:8000/api/store/store/2/" }'


def queue_callback(channel, method, properties, body):

    # Create a disctionary from message body
    message_json=json.loads(body.decode('utf-8'))
    
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
        logging.info( "requeued:", channel.basic_publish( RETRY_EXCHANGE, '', body ) )
    else:   
        # Fatal errors which can't be retried
        logging.error( "Fatal error creating Service charge" )
        logging.info( response.__dict__ )
            
    # Always ack (after work has completed) as retry handled via new message passed to retry exchange
    logging.info( "ackd:",channel.basic_ack(delivery_tag=method.delivery_tag, multiple=False))

        
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
    