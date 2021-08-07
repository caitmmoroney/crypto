# Imports
import os
from api import CoinbaseExchangeAuth, PublicCoinbaseAuth

# Environment variables
api_key = os.environ.get("API_KEY")
api_secret = os.environ.get("API_SECRET")
api_passphrase = os.environ.get("API_PASSPHRASE")
api_url = os.environ.get("API_URL")


auth = CoinbaseExchangeAuth(api_key, api_secret, api_passphrase, api_url)

# Get accounts
df = auth.getaccounts()
print(df)

publicAPI = PublicCoinbaseAuth(api_url)
print(f'The current price of Ethereum is: {publicAPI.getexchangeprice()}')

print(f'Products available on Coinbase Pro: {publicAPI.getproducts()}')


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
