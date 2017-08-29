from datetime import datetime, timedelta
import pickle

from xero import Xero
from xero.auth import PublicCredentials
from local_settings import CREDENTIALS

def get_credentials():
    try:
        with open( "credentials.pickle",'rb' ) as f :
            saved_state = pickle.load(f)
        credentials = PublicCredentials(**saved_state)
        if credentials.expired():
            raise ValueError('Credentials Expired')
    except( IOError, ValueError ):
        credentials = PublicCredentials(CREDENTIALS['KEY'],CREDENTIALS['SECRET'])
        print( credentials.url )
        token = input('url:')
        credentials.verify(token)

    with open( "credentials.pickle", 'wb' ) as f :
        pickle.dump(credentials.state,f, pickle.HIGHEST_PROTOCOL)
    
    return credentials


credentials = get_credentials()
xero = Xero(credentials)

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

result = xero.invoices.all()
#result = xero.invoices.put(data)
print( result )