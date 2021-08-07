# Imports
import base64
import hashlib
import hmac
from requests.auth import AuthBase
import time
import requests


# Define classes
# Taken straight from https://docs.pro.coinbase.com/?python#signing-a-message:

# Create custom authentication for Exchange
class CoinbaseExchangeAuth(AuthBase):
    def __init__(self, api_key, secret_key, passphrase):
        self.api_key = api_key
        self.secret_key = secret_key
        self.passphrase = passphrase

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


# Create class for accessing public API
class PublicCoinbaseAuth(AuthBase):
    def __init__(self, api_url):
        if api_url[-1] != '/':
            api_url = api_url + '/'
        self.api_url = api_url

    def getexchangeprice(self, market_symbol: str = 'ETH-USD'):
        rdict = requests.get(f'{self.api_url}products/{market_symbol}/ticker').json()

        return rdict['price']
