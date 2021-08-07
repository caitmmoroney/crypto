# Imports
import base64
import hashlib
import hmac
from requests.auth import AuthBase
import time
import requests
import pandas as pd


# Define classes
# Taken straight from https://docs.pro.coinbase.com/?python#signing-a-message:

# Create custom authentication for Exchange
class CoinbaseExchangeAuth(AuthBase):
    def __init__(self, api_key, secret_key, passphrase, api_url):
        self.api_key = api_key
        self.secret_key = secret_key
        self.passphrase = passphrase
        if api_url[-1] != '/':
            api_url = api_url + '/'
        self.api_url = api_url

    def __call__(self, request):
        timestamp = str(time.time())
        body = (
                request.body or b"").decode()  # this line taken from pycryptobot AuthAPI __call__ method (https://github.com/whittlem/pycryptobot/blob/main/models/exchange/coinbase_pro/api.py)
        message = timestamp + request.method + request.path_url + body
        hmac_key = base64.b64decode(self.secret_key)  # bytes object
        signature = hmac.new(hmac_key, message.encode(), digestmod=hashlib.sha256)
        signature_b64 = base64.b64encode(
            signature.digest()).decode()  # this line taken from pycrypto AuthAPI __call__ method

        request.headers.update({
            'CB-ACCESS-SIGN': signature_b64,
            'CB-ACCESS-TIMESTAMP': timestamp,
            'CB-ACCESS-KEY': self.api_key,
            'CB-ACCESS-PASSPHRASE': self.passphrase,
            'Content-Type': 'application/json'
        })
        return request

    def getaccounts(self):
        r = requests.get(self.api_url + 'accounts', auth=self)
        df = pd.DataFrame.from_dict(r.json())
        df = df[df.balance != '0.0000000000000000']
        df.reset_index(inplace=True, drop=True)

        return df

    def placeorder(self,
                   buy_or_sell: str = 'buy',
                   product_market: str = 'ETH-USD',
                   qty=1.0,
                   price=1.0):
        # validate product market
        products = PublicCoinbaseAuth(self.api_url).getproducts()

        if product_market not in products:
            print(f'The order could not be placed because the provided product exchange is not listed on Coinbase Pro.')
        else:
            order = {
                'size': qty,
                'price': price,
                'side': buy_or_sell,
                'product_id': product_market,
            }

            r = requests.post(self.api_url + 'orders', json=order, auth=self)
            print(f'Order ID: {r.json()["id"]}')

    def buyorder(self,
                 product_market: str = 'ETH-USD',
                 qty=1.0,
                 price=1.0):
        self.placeorder(buy_or_sell='buy',
                        product_market=product_market,
                        qty=qty,
                        price=price)

    def sellorder(self,
                 product_market: str = 'ETH-USD',
                 qty=1.0,
                 price=1.0):
        self.placeorder(buy_or_sell='sell',
                        product_market=product_market,
                        qty=qty,
                        price=price)

    def makedeposit(self,
                    bank: str,
                    account_last4digits: str,
                    amount=10.00,
                    currency: str = 'USD'):

        payment_methods = self.getpaymentmethods()
        payment_methods = payment_methods[payment_methods.allow_deposit == 'true']
        payment_methods.reset_index(drop=True, inplace=True)
        if any([el.startswith(bank) & el.endswith(account_last4digits) for el in payment_methods['name']]):
            selected_method = payment_methods[payment_methods['name'].startswith(bank) &
                                              payment_methods['name'].endswith(account_last4digits)]
            deposit = {
                "amount": amount,
                "currency": currency,
                "payment_method_id": selected_method
            }
            r = requests.post(self.api_url + 'deposits/payment-method', json=deposit, auth=self)
            print(f'Deposit ID: {r.json()["id"]}')
        else:
            print(f'Please specify a bank account which has withdraw permissions.')

    def getpaymentmethods(self):
        r = requests.get(self.api_url + 'payment-methods', auth=self)
        df = pd.DataFrame.from_dict(r.json())
        return df


# Create class for accessing public API
class PublicCoinbaseAuth(AuthBase):
    def __init__(self, api_url):
        if api_url[-1] != '/':
            api_url = api_url + '/'
        self.api_url = api_url

    def getexchangeprice(self, market_symbol: str = 'ETH-USD'):
        rdict = requests.get(f'{self.api_url}products/{market_symbol}/ticker').json()

        return rdict['price']

    def getproducts(self):
        rdict = requests.get(f'{self.api_url}products/').json()

        df = pd.DataFrame.from_dict(rdict)

        return df['id'].tolist()
