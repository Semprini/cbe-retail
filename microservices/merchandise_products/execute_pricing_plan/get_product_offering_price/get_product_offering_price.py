import json

from flask import Flask, request
app = Flask(__name__)

class RetryableError( Exception ):
    pass
    
class FatalError( Exception ):
    pass
    
def request(url, user, password, error_message):
    """
    A wrapper around the requests get function which will call CBE and load the json response.
    """
    if type(url) is dict:
        logging.info( "QueueTriggerPattern request called to get url but url is already dict. Assuming loaded json so returning input." )
        return url
    response = requests.get(url, auth=(user, password))
    if response.status_code >= 500 or response.status_code in (401,403):
        # Retryable errors which can be requeued
        logging.warning( "Retryable " + error_message + "{}".format(response.content) )
        raise RetryableError("Get {} returned: {}".format(url, response.status_code))
    elif response.status_code != 200:
        # Fatal errors which can't be retried
        logging.error( "Fatal " + error_message + "{}".format(response.content) )
        raise FatalError("Get {} returned: {}".format(url, response.status_code))
    return json.loads(response.text)


@app.route('/')
def get_product_offering_price():
    json = json.loads(request.get_data(as_text=True) )
    sale = request(json['sale'])
    offering = request(json['product_offering'])
    
    return 'Hello, World!'


example = """
{
    "type": "SaleItem",
    "url": "https://cbe.sphinx.co.nz/api/sale/sale_item/1/",
    "sale": "https://cbe.sphinx.co.nz/api/sale/sale/1/",
    "product_offering": "https://cbe.sphinx.co.nz/api/product/product_offering/243728/",
    "product": {
        "type": "Product",
        "url": "https://cbe.sphinx.co.nz/api/product/product/1/",
        "code": "243728",
        "name": "GAS CARTRIDGE BUTANE 220G 4 PACK NO. 8",
        "description": "",
        "bundle": [],
        "categories": [],
        "cross_sell_products": [],
        "product_offerings": [
            "https://cbe.sphinx.co.nz/api/product/product_offering/243728/"
        ]
    },
    "product_offering_price": null,
    "quantity": "1.0000",
    "unit_of_measure": "each",
    "amount": "8.68",
    "discount": "0.00",
    "promotion": null,
    "cost_price": "6.68"
}
"""