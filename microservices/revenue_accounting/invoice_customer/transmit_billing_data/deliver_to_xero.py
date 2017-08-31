import json
from datetime import datetime, timedelta
import pickle

import pika

from xero import Xero
from xero.auth import PublicCredentials
from local_settings import CREDENTIALS

QUEUE_HOST = "cbemq"
QUEUE_EXCHANGE = "notify.retail.customer_bill.CustomerBill.updated"
HTTP_HOST = "https://cbe.sphinx.co.nz"

test_json = '{{ "type": "CustomerBill", "url": "{0}/api/customer_bill/customer_bill/1/", "account": {{ "type": "CustomerAccount", "url": "{0}/api/customer/account/ZZBUCKLL/", "created": "2017-08-24", "valid_from": null, "valid_to": null, "customer": "{0}/api/customer/customer/ZZBUCKLL/", "account_number": "ZZBUCKLL", "account_status": "new", "managed_by": "{0}/api/party/organisation/1/", "credit_liabilities": [], "account_type": "", "name": "", "pin": null, "customer_account_contact": [] }}, "specification": "{0}/api/customer_bill/customer_bill_specification/1/", "customer": "{0}/api/customer/customer/ZZBUCKLL/", "number": "1", "created": "2017-08-24T21:54:37.190322Z", "period_from": "2017-08-24", "period_to": "2017-08-24", "status": "active", "amount": "10.00", "discounted": "0.00", "adjusted": "0.00", "rebated": "0.00", "disputed": "0.00", "allocated": "0.00", "accountbillitems": [], "jobbillitems": [ {{ "url": "{0}/api/customer_bill/job_bill_item/1/", "type": "JobBillItem", "job": {{ "type": "Job", "url": "{0}/api/job_management/job/1/", "created": "2017-08-29", "valid_from": null, "valid_to": null, "job_number": "1", "account": "{0}/api/customer/account/1234567/", "job_status": "active", "credit": null, "job_party_roles": [] }}, "item_type": "job", "amount": "10.00", "discounted": "0.00", "bill": "{0}/api/customer_bill/customer_bill/1/", "sale_events": [ "{0}/api/sale/sale/2/", "{0}/api/sale/sale/7/" ] }} ], "servicebillitems": [] }}'.format(HTTP_HOST)


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

    
def callback(ch, method, properties, body):
    # Create a disctionary from message body
    message_json=json.loads(body)
    account = message_json['account']['account_number']

    lineitems = []
    for item in message_json['jobbillitems']:
        lineitems.append(
            {
                'Description': 'Job %s'%item['job']['job_number'], 
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
    
    
def queue_setup(connection):
    channel = connection.channel()

    channel.exchange_declare(exchange=QUEUE_EXCHANGE, exchange_type='headers')

    result = channel.queue_declare(exclusive=True)
    if not result:
        print( 'Queue didnt declare properly!' )
        sys.exit(1)
    queue_name = result.method.queue

    channel.queue_bind(exchange=QUEUE_EXCHANGE, queue = queue_name, routing_key = '',arguments = {'status': 'active', }))
                       #arguments = {'ham': 'good', 'x-match':'any'})

    channel.basic_consume(callback, queue = queue_name, no_ack=True)
    return channel

    
def test_callback():
    callback(None, None, pika.BasicProperties(headers = {'foo':'a'}), test_json)

    
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
    
    
if __name__ == "__main__":
    test_callback()
    
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