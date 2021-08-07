# Imports
import os
import requests
from api import CoinbaseExchangeAuth, PublicCoinbaseAuth
import pandas as pd

# Environment variables
api_key = os.environ.get("API_KEY")
api_secret = os.environ.get("API_SECRET")
api_passphrase = os.environ.get("API_PASSPHRASE")
api_url = os.environ.get("API_URL")


auth = CoinbaseExchangeAuth(api_key, api_secret, api_passphrase)

# Get accounts
if api_url[-1] != '/':
    api_url = api_url + '/'
r = requests.get(api_url + 'accounts', auth=auth)
# print(r.json())
df = pd.DataFrame.from_dict(r.json())
df = df[df.balance != '0.0000000000000000']
df.reset_index(inplace=True, drop=True)
print(df)

publicAPI = PublicCoinbaseAuth(api_url)
print(f'The current price of Ethereum is: {publicAPI.getprice()}')
# {'message': 'NotFound'}


# # Place an order
# order = {
#     'size': 1.0,
#     'price': 1.0,
#     'side': 'buy',
#     'product_id': 'BTC-USD',
# }
# r = requests.post(api_url + 'orders', json=order, auth=auth)
# print r.json()
# # {"id": "0428b97b-bec1-429e-a94c-59992926778d"}
