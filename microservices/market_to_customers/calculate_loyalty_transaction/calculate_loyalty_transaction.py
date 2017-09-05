#!/usr/bin/env python 
import os, sys, time, json
import requests

import pika

QUEUE_HOST = "cbemq"
QUEUE_USER = "super"
QUEUE_PASS = "super"

EXCHANGES = ['notify.retail.sale.Sale.updated','notify.retail.sale.Sale.created',]
QUEUE = 'microservice.loyalty_transaction.Sale'

API_HOST = "https://cbe.sphinx.co.nz"
API_USER = "microservice"
API_PASS = "microservice"

LOYALTY_TRANSACTION_URL = API_HOST + "/api/loyalty/loyalty_transaction/"
LOYALTY_RATE = 0.01

test_json = b'{"type":"Sale","url":"http://127.0.0.1:8000/api/sale/sale/1/","channel":"http://127.0.0.1:8000/api/sale/sales_channel/1/","store":"http://127.0.0.1:8000/api/store/store/1/","seller":"http://127.0.0.1:8000/api/party/organisation/1/","datetime":"2000-01-01T07:25:00Z","docket_number":"1","total_amount":"9.98","total_amount_excl":"8.68","total_discount":"0.00","total_tax":"1.30","customer":"http://127.0.0.1:8000/api/customer/customer/1234567/","account":"http://127.0.0.1:8000/api/customer/account/1234567/","purchaser":null,"identification":"http://127.0.0.1:8000/api/human_resources/identification/1/","promotion":null,"till":"http://127.0.0.1:8000/api/resource/physical_resource/1/","staff":"http://127.0.0.1:8000/api/human_resources/staff/1/","price_channel":null,"price_calculation":null,"tenders":[{"type":"Tender","url":"http://127.0.0.1:8000/api/sale/tender/1/","sale":"http://127.0.0.1:8000/api/sale/sale/1/","tender_type":"http://127.0.0.1:8000/api/sale/tender_type/1/","amount":"9.98","reference":null}],"credit_balance_events":[],"sale_items":[{"type":"SaleItem","url":"http://127.0.0.1:8000/api/sale/sale_item/1/","sale":"http://127.0.0.1:8000/api/sale/sale/1/","product_offering":{"type":"ProductOffering","url":"http://127.0.0.1:8000/api/product/product_offering/1/","valid_from":null,"valid_to":null,"product":{"type":"Product","url":"http://127.0.0.1:8000/api/product/product/1/","valid_from":null,"valid_to":null,"name":"GAS CARTRIDGE BUTANE 220G 4 PACK NO. 8","description":"","unit_of_measure":"each","sku":"243728","bundle":[],"categories":[],"cross_sell_products":[]},"channels":["http://127.0.0.1:8000/api/sale/sales_channel/1/"],"segments":[],"strategies":[],"supplier_code":null,"retail_price":"9.98","product_offering_prices":["http://127.0.0.1:8000/api/price/product_offering_price/1/"],"supplier":null,"buyer":null},"amount":"8.68","discount":"0.00","promotion":null}]}'
loyalty_transaction_template = '{"scheme": "https://cbe.sphinx.co.nz/api/loyalty/loyalty_scheme/1/","promotion": null,"sale": "{SALE}","items": [],"loyalty_amount": {AMOUNT},"identification": "{ID}"}'

def queue_callback(ch, method, properties, body):
    # Create a disctionary from message body
    message_json=json.loads(body.decode('utf-8'))
    
    # If the customer swiped a card then add some airpoints
    if message_json['identification'] != None:
        print( "Sale with Airpoints triggered loyalty calc" )
        total=float(message_json['total_amount'])
        loyalty_amount = total * LOYALTY_RATE
        
        # Fill out LoyaltyTransaction json
        data = loyalty_transaction_template\
            .replace("{SALE}","{}".format(message_json['url']))\
            .replace('{AMOUNT}',"{:0.2f}".format(loyalty_amount))\
            .replace('{ID}',"{}".format(message_json['identification']))
            
        # Create a new LoyaltyTransaction transaction by calling API
        headers = {'Content-type': 'application/json',}
        response = requests.post(LOYALTY_TRANSACTION_URL, data=data, headers=headers, auth=(API_USER, API_PASS))
        if response.status_code == 201: # (201) Created
            print( "Loyalty transaction created" )
            ch.basic_ack(method.delivery_tag)
        else:
            print( "Error creating loyalty transaction" )
            print( response.__dict__ )
            ch.basic_nack(method.delivery_tag, multiple=False, requeue=True)
            #TODO: Fatal errors
    else:
        print("No ID in sale so no loyalty transaction created")
        

def queue_setup(connection, callback):
    channel = connection.channel()

    result = channel.queue_declare(exclusive=False, queue=QUEUE, durable=True )
    if not result:
        print( 'Queue didnt declare properly!' )
        sys.exit(1)

    for exchange in EXCHANGES:
        channel.exchange_declare(exchange=exchange, exchange_type='headers')
        channel.queue_bind(exchange=exchange, queue=QUEUE, routing_key = '',)
                       #arguments = {'ham': 'good', 'x-match':'any'})

    channel.basic_consume(callback, queue=QUEUE, no_ack=True)
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
                print( "Completed connection to MQ..." )
                ready = True
            except KeyboardInterrupt:
                ready = True
                done = True
            except:
                print( "Connection to MQ not ready, retry..." )
                time.sleep(5)
        try:
           queue_setup(connection, queue_callback).start_consuming()
        except pika.exceptions.ConnectionClosed:
            print( "Connection to MQ closed. retry..." )
            connection = None
            ready = False
            time.sleep(5)
        except KeyboardInterrupt:
            print( 'Bye' )
            done = True
        finally:
            if connection:
                connection.close()

            
if __name__ == "__main__":
    #test handler:
    #queue_callback(None, None, pika.BasicProperties(headers = {'foo':'a'}), test_json)
    
    main(os.environ['QUEUE_HOST'],os.environ['QUEUE_USER'],os.environ['QUEUE_PASS'])
    