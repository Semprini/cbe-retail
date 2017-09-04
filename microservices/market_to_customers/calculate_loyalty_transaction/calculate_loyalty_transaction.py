#!/usr/bin/env python 
import sys, time, json
import requests

import pika

QUEUE_HOST = "cbemq"
QUEUE_USER = "super"
QUEUE_PASS = "super"

LOYALTY_TRANSACTION_URL = "https://cbe.sphinx.co.nz/api/loyalty/loyalty_transaction/"
LOYALTY_RATE = 0.01

test_json = b'{"type":"Sale","url":"http://127.0.0.1:8000/api/sale/sale/1/","channel":"http://127.0.0.1:8000/api/sale/sales_channel/1/","store":"http://127.0.0.1:8000/api/store/store/1/","seller":"http://127.0.0.1:8000/api/party/organisation/1/","datetime":"2000-01-01T07:25:00Z","docket_number":"1","total_amount":"9.98","total_amount_excl":"8.68","total_discount":"0.00","total_tax":"1.30","customer":"http://127.0.0.1:8000/api/customer/customer/1234567/","account":"http://127.0.0.1:8000/api/customer/account/1234567/","purchaser":null,"identification":"http://127.0.0.1:8000/api/human_resources/identification/1/","promotion":null,"till":"http://127.0.0.1:8000/api/resource/physical_resource/1/","staff":"http://127.0.0.1:8000/api/human_resources/staff/1/","price_channel":null,"price_calculation":null,"tenders":[{"type":"Tender","url":"http://127.0.0.1:8000/api/sale/tender/1/","sale":"http://127.0.0.1:8000/api/sale/sale/1/","tender_type":"http://127.0.0.1:8000/api/sale/tender_type/1/","amount":"9.98","reference":null}],"credit_balance_events":[],"sale_items":[{"type":"SaleItem","url":"http://127.0.0.1:8000/api/sale/sale_item/1/","sale":"http://127.0.0.1:8000/api/sale/sale/1/","product_offering":{"type":"ProductOffering","url":"http://127.0.0.1:8000/api/product/product_offering/1/","valid_from":null,"valid_to":null,"product":{"type":"Product","url":"http://127.0.0.1:8000/api/product/product/1/","valid_from":null,"valid_to":null,"name":"GAS CARTRIDGE BUTANE 220G 4 PACK NO. 8","description":"","unit_of_measure":"each","sku":"243728","bundle":[],"categories":[],"cross_sell_products":[]},"channels":["http://127.0.0.1:8000/api/sale/sales_channel/1/"],"segments":[],"strategies":[],"supplier_code":null,"retail_price":"9.98","product_offering_prices":["http://127.0.0.1:8000/api/price/product_offering_price/1/"],"supplier":null,"buyer":null},"amount":"8.68","discount":"0.00","promotion":null}]}'
loyalty_transaction_template = '{"scheme": "https://cbe.sphinx.co.nz/api/loyalty/loyalty_scheme/1/","promotion": null,"sale": "{SALE}","items": [],"loyalty_amount": {AMOUNT},"identification": "{ID}"}'

def callback(ch, method, properties, body):
    # Create a disctionary from message body
    message_json=json.loads(body)
    
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
        response = requests.post(LOYALTY_TRANSACTION_URL, data=data, headers=headers, auth=('super', 'super'))
        if response.status_code != 201: # (201) Created
            print( "Error creating loyalty transaction" )
            print( response.__dict__ )
        else:
            print( "Loyalty transaction created" )
    else:
        print("No ID in sale so no loyalty transaction created")
        

def queue_setup(connection):
    channel = connection.channel()

    channel.exchange_declare(exchange='notify.retail.sale.Sale.updated', exchange_type='headers')

    result = channel.queue_declare(exclusive=True)
    if not result:
        print( 'Queue didnt declare properly!' )
        sys.exit(1)
    queue_name = result.method.queue

    channel.queue_bind(exchange='notify.retail.sale.Sale.updated', queue = queue_name, routing_key = '',)
                       #arguments = {'ham': 'good', 'x-match':'any'})

    channel.basic_consume(callback, queue = queue_name, no_ack=True)
    return channel
    

def main(host,user,password):
    credentials = pika.PlainCredentials(user, password)
    connection = None
    ready = False
    while not ready:
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(host=host, credentials=credentials))
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

            
if __name__ == "__main__":
    #test handler:
    #callback(None, None, pika.BasicProperties(headers = {'foo':'a'}), test_json)
    
    main(QUEUE_HOST,QUEUE_USER,QUEUE_PASS)
    