#!/usr/bin/env python 
import sys, time, json
import requests

import pika

QUEUE_HOST = "cbemq"
HTTP_HOST = "https://cbe.sphinx.co.nz"
SERVICE_CHARGE_URL = HTTP_HOST + "/api/customer_bill/service_charge/"
RATE = 0.5

test_json = '{{ "type": "CustomerBill", "url": "{0}/api/customer_bill/customer_bill/1/",     "number": "1",     "created": "2017-08-24T21:43:42.312476Z",     "period_from": "2017-08-24",     "period_to": "2017-08-24",     "status": "active",     "amount": "0.00",     "discounted": "0.00",     "adjusted": "0.00",     "rebated": "0.00",     "disputed": "0.00",     "allocated": "0.00",     "account": {{ "type": "CustomerAccount", "url": "{0}/api/customer/account/ZZBUCKLL/", "created": "2017-08-24", "valid_from": null, "valid_to": null, "customer": "{0}/api/customer/customer/ZZBUCKLL/", "account_number": "ZZBUCKLL",         "account_status": "new",         "managed_by": "{0}/api/party/organisation/1/",         "credit_liabilities": [],         "account_type": "",         "name": "",         "pin": null,         "customer_account_contact": []     }},     "specification": "{0}/api/customer_bill/customer_bill_specification/1/",     "accountbillitems": [],     "jobbillitems": [] }}'.format(HTTP_HOST)
service_charge_template = '{ "total_margin": "{TOTAL_MARGIN}", "home_margin": "{HOME_MARGIN}", "satellite_margin": "{SATELLITE_MARGIN}", "bill": "{BILL}", "service_bill_item": null, "sale": "http://127.0.0.1:8000/api/sale/sale/1/", "home_store": "http://127.0.0.1:8000/api/store/store/1/", "satellite_store": "http://127.0.0.1:8000/api/store/store/2/" }'

def callback(ch, method, properties, body):
    # Create a disctionary from message body
    message_json=json.loads(body)
    
    total=float(message_json['amount'])
    
    # Fill out LoyaltyTransaction json
    data = service_charge_template\
        .replace("{BILL}","{}".format(message_json['url']))\
        .replace('{TOTAL_MARGIN}',"{:0.2f}".format(total))\
        .replace('{HOME_MARGIN}',"{:0.2f}".format(total/RATE))\
        .replace('{SATELLITE_MARGIN}',"{:0.2f}".format(total-(total/RATE)))
        
    # Create a new LoyaltyTransaction transaction by calling API
    headers = {'Content-type': 'application/json',}
    response = requests.post(SERVICE_CHARGE_URL, data=data, headers=headers, auth=('super', 'super'))
    if response.status_code != 201: # (201) Created
        print( "Error creating service charge. ({}) - {}".format( response.status_code,response.reason ) )
    else:
        print( "Service charge created" )
        

def queue_setup(connection):
    channel = connection.channel()

    channel.exchange_declare(exchange='notify.retail.customer_bill.CustomerBill.updated', type='headers')

    result = channel.queue_declare(exclusive=True)
    if not result:
        print( 'Queue didnt declare properly!' )
        sys.exit(1)
    queue_name = result.method.queue

    channel.queue_bind(exchange='notify.retail.customer_bill.CustomerBill.updated', queue = queue_name, routing_key = '',)
                       #arguments = {'ham': 'good', 'x-match':'any'})

    channel.basic_consume(callback, queue = queue_name, no_ack=True)
    return channel
    
    
if __name__ == "__main__":
    #test handler:
    #callback(None, None, pika.BasicProperties(headers = {'foo':'a'}), test_json)
    
    connection = None
    ready = False
    while not ready:
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(host=QUEUE_HOST))
            print( "Completed connection to MQ..." )
            ready = True
        except KeyboardInterrupt:
            ready = True
        except:
            print( "Connection to MQ not ready, retry..." )
            time.sleep(5)
    try:
       queue_setup(connection).start_consuming()
    except KeyboardInterrupt:
        print( 'Bye' )
    finally:
        if connection:
            connection.close()
        