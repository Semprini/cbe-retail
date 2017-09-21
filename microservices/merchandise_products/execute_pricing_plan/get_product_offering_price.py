from flask import Flask
app = Flask(__name__)

@app.route('/')
def get_product_offering_price():
    return 'Hello, World!'
