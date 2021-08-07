# Imports
# from coinbase.wallet.client import Client
import base64
import hashlib
import hmac
import os
import requests
import time

from requests.auth import AuthBase

# Environment variables
api_key = os.environ.get("API_KEY")
api_secret = os.environ.get("API_SECRET")
api_passphrase = os.environ.get("API_PASSPHRASE")
api_url = os.environ.get("API_URL")

# client = Client(api_key, api_secret)
# currency = 'USD'
# start_price = client.get_spot_price(currency=currency)
# print(f'Start price is: {start_price.amount}')


# Taken straight from https://docs.pro.coinbase.com/?python#signing-a-message:

# Create custom authentication for Exchange
class CoinbaseExchangeAuth(AuthBase):
    def __init__(self, api_key, secret_key, passphrase):
        self.api_key = api_key
        self.secret_key = secret_key
        self.passphrase = passphrase

    def __call__(self, request):
        timestamp = str(time.time())
        body = (request.body or b"").decode() # this line taken from pycryptobot AuthAPI __call__ method (https://github.com/whittlem/pycryptobot/blob/main/models/exchange/coinbase_pro/api.py)
        message = timestamp + request.method + request.path_url + body
        hmac_key = base64.b64decode(self.secret_key) # bytes object
        signature = hmac.new(hmac_key, message.encode(), digestmod=hashlib.sha256)
        signature_b64 = base64.b64encode(signature.digest()).decode() # this line taken from pycrypto AuthAPI __call__ method

        request.headers.update({
            'CB-ACCESS-SIGN': signature_b64,
            'CB-ACCESS-TIMESTAMP': timestamp,
            'CB-ACCESS-KEY': self.api_key,
            'CB-ACCESS-PASSPHRASE': self.passphrase,
            'Content-Type': 'application/json'
        })
        return request


auth = CoinbaseExchangeAuth(api_key, api_secret, api_passphrase)

# Get accounts
if api_url[-1] != '/':
    api_url = api_url + '/'
r = requests.get(api_url + 'accounts', auth=auth)
print(r.json())
# [{'id': '03c8f347-f0ad-4141-8b74-6420b6e6b780', 'currency': '1INCH', 'balance': '0.0000000000000000',
# 'hold': '0.0000000000000000', 'available': '0', 'profile_id': 'c6376665-d9a9-48f7-9af9-e99491b91b87',
# 'trading_enabled': True}, {'id': '0a78c881-dbc2-4e7c-b69c-e9ce7c97ad95', 'currency': 'AAVE', 'balance':
# '0.0000000000000000', 'hold': '0.0000000000000000', 'available': '0', 'profile_id':
# 'c6376665-d9a9-48f7-9af9-e99491b91b87', 'trading_enabled': True}, {'id': '98738015-d0c9-46ea-a32c-4a27878a7078',
# 'currency': 'ACH', 'balance': '0.0000000000000000', 'hold': '0.0000000000000000', 'available': '0', 'profile_id':
# 'c6376665-d9a9-48f7-9af9-e99491b91b87', 'trading_enabled': True}, {'id': '404e63b5-f10e-4467-b553-1b5cf8daf178',
# 'currency': 'ADA', 'balance': '18.9400000000000000', 'hold': '0.0000000000000000', 'available': '18.94',
# 'profile_id': 'c6376665-d9a9-48f7-9af9-e99491b91b87', 'trading_enabled': True},
# {'id': 'c716c441-706a-4651-9e1a-52e955233a9e', 'currency': 'ALGO', 'balance': '23.4458260000000000',
# 'hold': '0.0000000000000000', 'available': '23.445826', 'profile_id': 'c6376665-d9a9-48f7-9af9-e99491b91b87',
# 'trading_enabled': True}, {'id': '1d7e8b6e-9389-4944-98f8-53c44e95bc09', 'currency': 'AMP', 'balance':
# '0.0000000000000000', 'hold': '0.0000000000000000', 'available': '0', 'profile_id':
# 'c6376665-d9a9-48f7-9af9-e99491b91b87', 'trading_enabled': True}, {'id': '32c54621-79ac-4b31-ad34-99c068c374df',
# 'currency': 'ANKR', 'balance': '0.0000000000000000', 'hold': '0.0000000000000000', 'available': '0', 'profile_id':
# 'c6376665-d9a9-48f7-9af9-e99491b91b87', 'trading_enabled': True}, {'id': 'f57ff06b-ba11-4bd0-8314-f6e81e5539b2',
# 'currency': 'ATOM', 'balance': '0.7000760000000000', 'hold': '0.0000000000000000', 'available': '0.700076',
# 'profile_id': 'c6376665-d9a9-48f7-9af9-e99491b91b87', 'trading_enabled': True},
# {'id': '8a8e5960-2459-43f7-a937-de7f20e99e68', 'currency': 'BAL', 'balance': '0.0000000000000000',
# 'hold': '0.0000000000000000', 'available': '0', 'profile_id': 'c6376665-d9a9-48f7-9af9-e99491b91b87',
# 'trading_enabled': True}, {'id': 'c7ef92e3-1aed-4cd6-b692-e73a52b29e2f', 'currency': 'BAND', 'balance':
# '0.0000000000000000', 'hold': '0.0000000000000000', 'available': '0', 'profile_id':
# 'c6376665-d9a9-48f7-9af9-e99491b91b87', 'trading_enabled': True}, {'id': '87fb33e5-8d48-46ab-b9e9-88b1ee4a458e',
# 'currency': 'BAT', 'balance': '0.0000000000000000', 'hold': '0.0000000000000000', 'available': '0', 'profile_id':
# 'c6376665-d9a9-48f7-9af9-e99491b91b87', 'trading_enabled': True}, {'id': '533dc063-6b58-4001-91e7-7c7a5c39abb6',
# 'currency': 'BCH', 'balance': '0.0000000000000000', 'hold': '0.0000000000000000', 'available': '0', 'profile_id':
# 'c6376665-d9a9-48f7-9af9-e99491b91b87', 'trading_enabled': True}, {'id': '3fd3623b-7e5c-41a4-b96e-0d218c7be1d6',
# 'currency': 'BNT', 'balance': '0.0000000000000000', 'hold': '0.0000000000000000', 'available': '0', 'profile_id':
# 'c6376665-d9a9-48f7-9af9-e99491b91b87', 'trading_enabled': True}, {'id': '9ccefe4f-7d21-4a52-b391-9a1a74d13d8c',
# 'currency': 'BOND', 'balance': '0.0000000000000000', 'hold': '0.0000000000000000', 'available': '0', 'profile_id':
# 'c6376665-d9a9-48f7-9af9-e99491b91b87', 'trading_enabled': True}, {'id': 'c43f0269-1909-4603-89d3-582ec6797983',
# 'currency': 'BTC', 'balance': '0.0036920400000000', 'hold': '0.0000000000000000', 'available': '0.00369204',
# 'profile_id': 'c6376665-d9a9-48f7-9af9-e99491b91b87', 'trading_enabled': True},
# {'id': '7cdf7b14-e00f-4722-bcd1-93039f8ddca4', 'currency': 'CGLD', 'balance': '0.0000000000000000',
# 'hold': '0.0000000000000000', 'available': '0', 'profile_id': 'c6376665-d9a9-48f7-9af9-e99491b91b87',
# 'trading_enabled': True}, {'id': 'faf5db16-c33b-484e-b21b-94c80f2d558f', 'currency': 'CHZ', 'balance':
# '236.0000000000000000', 'hold': '0.0000000000000000', 'available': '236', 'profile_id':
# 'c6376665-d9a9-48f7-9af9-e99491b91b87', 'trading_enabled': True}, {'id': '4276d462-3d05-49a6-b3d9-0b787807fcd5',
# 'currency': 'CLV', 'balance': '0.0000000000000000', 'hold': '0.0000000000000000', 'available': '0', 'profile_id':
# 'c6376665-d9a9-48f7-9af9-e99491b91b87', 'trading_enabled': True}, {'id': '8f2092c9-a15b-4b89-bbe4-f32e0521e89d',
# 'currency': 'COMP', 'balance': '0.0000000000000000', 'hold': '0.0000000000000000', 'available': '0', 'profile_id':
# 'c6376665-d9a9-48f7-9af9-e99491b91b87', 'trading_enabled': True}, {'id': '1fab9d6b-b648-4a24-99cf-7a5aab149888',
# 'currency': 'CRV', 'balance': '0.0000000000000000', 'hold': '0.0000000000000000', 'available': '0', 'profile_id':
# 'c6376665-d9a9-48f7-9af9-e99491b91b87', 'trading_enabled': True}, {'id': 'aff82f71-c0eb-4463-98f5-e83c74c9466d',
# 'currency': 'CTSI', 'balance': '0.0000000000000000', 'hold': '0.0000000000000000', 'available': '0', 'profile_id':
# 'c6376665-d9a9-48f7-9af9-e99491b91b87', 'trading_enabled': True}, {'id': 'fe18b42c-f9c1-4702-aa5c-93a00100095b',
# 'currency': 'CVC', 'balance': '0.0000000000000000', 'hold': '0.0000000000000000', 'available': '0', 'profile_id':
# 'c6376665-d9a9-48f7-9af9-e99491b91b87', 'trading_enabled': True}, {'id': 'c836724a-93c3-492e-a4e9-1020c6ea3153',
# 'currency': 'DAI', 'balance': '0.0000000000000000', 'hold': '0.0000000000000000', 'available': '0', 'profile_id':
# 'c6376665-d9a9-48f7-9af9-e99491b91b87', 'trading_enabled': True}, {'id': 'e50fb766-8ed0-4763-bbff-e3ebab55f191',
# 'currency': 'DASH', 'balance': '0.0798395800000000', 'hold': '0.0000000000000000', 'available': '0.07983958',
# 'profile_id': 'c6376665-d9a9-48f7-9af9-e99491b91b87', 'trading_enabled': True},
# {'id': '8315e9c8-81b6-4802-9aa1-db9909c538e6', 'currency': 'DNT', 'balance': '0.0000000000000000',
# 'hold': '0.0000000000000000', 'available': '0', 'profile_id': 'c6376665-d9a9-48f7-9af9-e99491b91b87',
# 'trading_enabled': True}, {'id': 'c58a95f9-e736-4e4a-ae6b-3aab38e027c5', 'currency': 'DOGE', 'balance':
# '96.4000000000000000', 'hold': '0.0000000000000000', 'available': '96.4', 'profile_id':
# 'c6376665-d9a9-48f7-9af9-e99491b91b87', 'trading_enabled': True}, {'id': '30c8252f-daeb-411e-9e3d-c19c5eff689c',
# 'currency': 'DOT', 'balance': '0.0000000000000000', 'hold': '0.0000000000000000', 'available': '0', 'profile_id':
# 'c6376665-d9a9-48f7-9af9-e99491b91b87', 'trading_enabled': True}, {'id': '727ae1c7-2948-41e1-813d-5bdcee3ddd97',
# 'currency': 'ENJ', 'balance': '0.0000000000000000', 'hold': '0.0000000000000000', 'available': '0', 'profile_id':
# 'c6376665-d9a9-48f7-9af9-e99491b91b87', 'trading_enabled': True}, {'id': '71da0533-42bc-46a0-87d9-07886ea6b4c6',
# 'currency': 'EOS', 'balance': '0.0000000000000000', 'hold': '0.0000000000000000', 'available': '0', 'profile_id':
# 'c6376665-d9a9-48f7-9af9-e99491b91b87', 'trading_enabled': True}, {'id': 'c05d4fc4-8df1-4a2b-b2ab-687a7ff7be8f',
# 'currency': 'ETC', 'balance': '0.0000000000000000', 'hold': '0.0000000000000000', 'available': '0', 'profile_id':
# 'c6376665-d9a9-48f7-9af9-e99491b91b87', 'trading_enabled': True}, {'id': 'e3b2a5ce-122d-414d-ac8a-0bf0acfac2d4',
# 'currency': 'ETH', 'balance': '0.1346233300000000', 'hold': '0.0000000000000000', 'available': '0.13462333',
# 'profile_id': 'c6376665-d9a9-48f7-9af9-e99491b91b87', 'trading_enabled': True},
# {'id': 'fd89a158-1dd8-4cf7-a705-773ac50d9690', 'currency': 'FARM', 'balance': '0.0000000000000000',
# 'hold': '0.0000000000000000', 'available': '0', 'profile_id': 'c6376665-d9a9-48f7-9af9-e99491b91b87',
# 'trading_enabled': True}, {'id': 'bfc0709f-9ebe-4936-ada6-eb3e7f2cdf32', 'currency': 'FET', 'balance':
# '0.0000000000000000', 'hold': '0.0000000000000000', 'available': '0', 'profile_id':
# 'c6376665-d9a9-48f7-9af9-e99491b91b87', 'trading_enabled': True}, {'id': '5e7c830b-9390-4bcc-a5de-154ffd9da954',
# 'currency': 'FIL', 'balance': '0.0000000000000000', 'hold': '0.0000000000000000', 'available': '0', 'profile_id':
# 'c6376665-d9a9-48f7-9af9-e99491b91b87', 'trading_enabled': True}, {'id': '6f28bb78-6a63-481d-b6fb-27daa60801d6',
# 'currency': 'FORTH', 'balance': '0.0000000000000000', 'hold': '0.0000000000000000', 'available': '0', 'profile_id':
# 'c6376665-d9a9-48f7-9af9-e99491b91b87', 'trading_enabled': True}, {'id': '5b987ac2-5353-45d1-895c-5cf55712c558',
# 'currency': 'GNT', 'balance': '0.0000000000000000', 'hold': '0.0000000000000000', 'available': '0', 'profile_id':
# 'c6376665-d9a9-48f7-9af9-e99491b91b87', 'trading_enabled': True}, {'id': '604c201d-2f7c-4d17-81b2-e32f78dbdfa5',
# 'currency': 'GRT', 'balance': '0.0000000000000000', 'hold': '0.0000000000000000', 'available': '0', 'profile_id':
# 'c6376665-d9a9-48f7-9af9-e99491b91b87', 'trading_enabled': True}, {'id': 'd0aeb199-cd84-4777-af5b-f606e3cee91a',
# 'currency': 'GTC', 'balance': '0.0000000000000000', 'hold': '0.0000000000000000', 'available': '0', 'profile_id':
# 'c6376665-d9a9-48f7-9af9-e99491b91b87', 'trading_enabled': True}, {'id': '6043d758-6277-4393-8bef-04218835f3c9',
# 'currency': 'ICP', 'balance': '0.0000000000000000', 'hold': '0.0000000000000000', 'available': '0', 'profile_id':
# 'c6376665-d9a9-48f7-9af9-e99491b91b87', 'trading_enabled': True}, {'id': 'bcc0edf7-93d0-423d-a254-f2013fe73427',
# 'currency': 'KEEP', 'balance': '0.0000000000000000', 'hold': '0.0000000000000000', 'available': '0', 'profile_id':
# 'c6376665-d9a9-48f7-9af9-e99491b91b87', 'trading_enabled': True}, {'id': '66e67e9a-2592-4523-bc75-12d248445cee',
# 'currency': 'KNC', 'balance': '0.0000000000000000', 'hold': '0.0000000000000000', 'available': '0', 'profile_id':
# 'c6376665-d9a9-48f7-9af9-e99491b91b87', 'trading_enabled': True}, {'id': '3658dd27-43be-4aa7-94a8-9692f452ef3c',
# 'currency': 'LINK', 'balance': '0.0000000000000000', 'hold': '0.0000000000000000', 'available': '0', 'profile_id':
# 'c6376665-d9a9-48f7-9af9-e99491b91b87', 'trading_enabled': True}, {'id': 'dcfedc86-453f-4191-9248-909e0c76bef1',
# 'currency': 'LOOM', 'balance': '0.0000000000000000', 'hold': '0.0000000000000000', 'available': '0', 'profile_id':
# 'c6376665-d9a9-48f7-9af9-e99491b91b87', 'trading_enabled': True}, {'id': '92dda332-00dc-4047-b38a-019dc61314a2',
# 'currency': 'LPT', 'balance': '0.0000000000000000', 'hold': '0.0000000000000000', 'available': '0', 'profile_id':
# 'c6376665-d9a9-48f7-9af9-e99491b91b87', 'trading_enabled': True}, {'id': '82e35c10-efcb-4d31-ae17-3afabc56a9f7',
# 'currency': 'LRC', 'balance': '0.0000000000000000', 'hold': '0.0000000000000000', 'available': '0', 'profile_id':
# 'c6376665-d9a9-48f7-9af9-e99491b91b87', 'trading_enabled': True}, {'id': '20a83b6e-0d0c-4fcb-a23e-e86884deae19',
# 'currency': 'LTC', 'balance': '0.0657319000000000', 'hold': '0.0000000000000000', 'available': '0.0657319',
# 'profile_id': 'c6376665-d9a9-48f7-9af9-e99491b91b87', 'trading_enabled': True},
# {'id': 'c7a00ac7-738a-4442-9cf2-51c2ddec49c9', 'currency': 'MANA', 'balance': '19.1300000000000000',
# 'hold': '0.0000000000000000', 'available': '19.13', 'profile_id': 'c6376665-d9a9-48f7-9af9-e99491b91b87',
# 'trading_enabled': True}, {'id': 'd8b641fe-8b78-4dc2-ab9a-ab35fc76f833', 'currency': 'MASK', 'balance':
# '0.0000000000000000', 'hold': '0.0000000000000000', 'available': '0', 'profile_id':
# 'c6376665-d9a9-48f7-9af9-e99491b91b87', 'trading_enabled': True}, {'id': 'c3f43b77-78fe-4f80-ba21-64938b504c9f',
# 'currency': 'MATIC', 'balance': '0.0000000000000000', 'hold': '0.0000000000000000', 'available': '0', 'profile_id':
# 'c6376665-d9a9-48f7-9af9-e99491b91b87', 'trading_enabled': True}, {'id': '61405585-a009-4939-a168-4fb5fc670fea',
# 'currency': 'MIR', 'balance': '0.0000000000000000', 'hold': '0.0000000000000000', 'available': '0', 'profile_id':
# 'c6376665-d9a9-48f7-9af9-e99491b91b87', 'trading_enabled': True}, {'id': 'a14c8127-c803-453b-b1dc-124acdd834d6',
# 'currency': 'MKR', 'balance': '0.0000000000000000', 'hold': '0.0000000000000000', 'available': '0', 'profile_id':
# 'c6376665-d9a9-48f7-9af9-e99491b91b87', 'trading_enabled': True}, {'id': 'd7029997-4787-4d04-8213-8109a8f1c8f5',
# 'currency': 'MLN', 'balance': '0.0000000000000000', 'hold': '0.0000000000000000', 'available': '0', 'profile_id':
# 'c6376665-d9a9-48f7-9af9-e99491b91b87', 'trading_enabled': True}, {'id': 'e9e6fd79-517c-42ae-85fd-69e428ab2a61',
# 'currency': 'NKN', 'balance': '0.0000000000000000', 'hold': '0.0000000000000000', 'available': '0', 'profile_id':
# 'c6376665-d9a9-48f7-9af9-e99491b91b87', 'trading_enabled': True}, {'id': '2c0d9c68-f528-4cdc-84af-673523e7ae7c',
# 'currency': 'NMR', 'balance': '0.0000000000000000', 'hold': '0.0000000000000000', 'available': '0', 'profile_id':
# 'c6376665-d9a9-48f7-9af9-e99491b91b87', 'trading_enabled': True}, {'id': '6c5eec5b-28f5-4f53-bebf-43cbcae240bd',
# 'currency': 'NU', 'balance': '0.0000000000000000', 'hold': '0.0000000000000000', 'available': '0', 'profile_id':
# 'c6376665-d9a9-48f7-9af9-e99491b91b87', 'trading_enabled': True}, {'id': 'bd6493cb-76d3-4aa3-87b8-5dbf172790ee',
# 'currency': 'OGN', 'balance': '0.0000000000000000', 'hold': '0.0000000000000000', 'available': '0', 'profile_id':
# 'c6376665-d9a9-48f7-9af9-e99491b91b87', 'trading_enabled': True}, {'id': '3ef7ca2b-f392-48c6-965a-89d433735506',
# 'currency': 'OMG', 'balance': '0.0000000000000000', 'hold': '0.0000000000000000', 'available': '0', 'profile_id':
# 'c6376665-d9a9-48f7-9af9-e99491b91b87', 'trading_enabled': True}, {'id': 'd7ea23de-7d99-4286-ac08-ea30ac4ff8c5',
# 'currency': 'OXT', 'balance': '0.0000000000000000', 'hold': '0.0000000000000000', 'available': '0', 'profile_id':
# 'c6376665-d9a9-48f7-9af9-e99491b91b87', 'trading_enabled': True}, {'id': 'ccecfa8f-5e7e-443b-a576-3d62928f16a7',
# 'currency': 'PAX', 'balance': '0.0000000000000000', 'hold': '0.0000000000000000', 'available': '0', 'profile_id':
# 'c6376665-d9a9-48f7-9af9-e99491b91b87', 'trading_enabled': True}, {'id': '9deb8a5f-2659-48b9-a05e-5e7f8a8ce64a',
# 'currency': 'PLA', 'balance': '0.0000000000000000', 'hold': '0.0000000000000000', 'available': '0', 'profile_id':
# 'c6376665-d9a9-48f7-9af9-e99491b91b87', 'trading_enabled': True}, {'id': '70b1cfdc-c046-453e-88ad-6a43df58baad',
# 'currency': 'POLY', 'balance': '0.0000000000000000', 'hold': '0.0000000000000000', 'available': '0', 'profile_id':
# 'c6376665-d9a9-48f7-9af9-e99491b91b87', 'trading_enabled': True}, {'id': 'beb093e6-57c1-4179-bc7f-a546f5541142',
# 'currency': 'QNT', 'balance': '0.0000000000000000', 'hold': '0.0000000000000000', 'available': '0', 'profile_id':
# 'c6376665-d9a9-48f7-9af9-e99491b91b87', 'trading_enabled': True}, {'id': '04cf583c-77ab-4781-8319-d9de1b628975',
# 'currency': 'RAI', 'balance': '0.0000000000000000', 'hold': '0.0000000000000000', 'available': '0', 'profile_id':
# 'c6376665-d9a9-48f7-9af9-e99491b91b87', 'trading_enabled': True}, {'id': '33413499-1eb8-44f9-9071-7bb8bf9ec7c0',
# 'currency': 'REN', 'balance': '0.0000000000000000', 'hold': '0.0000000000000000', 'available': '0', 'profile_id':
# 'c6376665-d9a9-48f7-9af9-e99491b91b87', 'trading_enabled': True}, {'id': '811da951-7042-4f49-a440-2de987da5f14',
# 'currency': 'REP', 'balance': '0.0000000000000000', 'hold': '0.0000000000000000', 'available': '0', 'profile_id':
# 'c6376665-d9a9-48f7-9af9-e99491b91b87', 'trading_enabled': True}, {'id': '84dee890-cbd1-4e26-8842-08f62292c5dc',
# 'currency': 'RLC', 'balance': '0.0000000000000000', 'hold': '0.0000000000000000', 'available': '0', 'profile_id':
# 'c6376665-d9a9-48f7-9af9-e99491b91b87', 'trading_enabled': True}, {'id': '4add559f-c26e-4ece-9be9-c172f410133d',
# 'currency': 'RLY', 'balance': '0.0000000000000000', 'hold': '0.0000000000000000', 'available': '0', 'profile_id':
# 'c6376665-d9a9-48f7-9af9-e99491b91b87', 'trading_enabled': True}, {'id': 'd4debf41-baab-43f3-98d8-ac90f411bfb5',
# 'currency': 'SHIB', 'balance': '0.0000000000000000', 'hold': '0.0000000000000000', 'available': '0', 'profile_id':
# 'c6376665-d9a9-48f7-9af9-e99491b91b87', 'trading_enabled': True}, {'id': '219937ce-7ba2-40e8-b30c-6194d6417509',
# 'currency': 'SKL', 'balance': '0.0000000000000000', 'hold': '0.0000000000000000', 'available': '0', 'profile_id':
# 'c6376665-d9a9-48f7-9af9-e99491b91b87', 'trading_enabled': True}, {'id': '2849c9bb-d81d-4853-aa12-12906395fb5f',
# 'currency': 'SNX', 'balance': '0.0000000000000000', 'hold': '0.0000000000000000', 'available': '0', 'profile_id':
# 'c6376665-d9a9-48f7-9af9-e99491b91b87', 'trading_enabled': True}, {'id': 'a36ac5a1-c912-45c5-bce2-137761c46a77',
# 'currency': 'SOL', 'balance': '0.0000000000000000', 'hold': '0.0000000000000000', 'available': '0', 'profile_id':
# 'c6376665-d9a9-48f7-9af9-e99491b91b87', 'trading_enabled': True}, {'id': '42ccb9b1-249a-46c3-b707-0cb230de1758',
# 'currency': 'STORJ', 'balance': '0.0000000000000000', 'hold': '0.0000000000000000', 'available': '0', 'profile_id':
# 'c6376665-d9a9-48f7-9af9-e99491b91b87', 'trading_enabled': True}, {'id': '75c94365-15d9-4f08-86bd-4d5626a08236',
# 'currency': 'SUSHI', 'balance': '0.0000000000000000', 'hold': '0.0000000000000000', 'available': '0', 'profile_id':
# 'c6376665-d9a9-48f7-9af9-e99491b91b87', 'trading_enabled': True}, {'id': 'c34904df-4f58-4e66-bd24-53e24fe1a3c6',
# 'currency': 'TRB', 'balance': '0.0000000000000000', 'hold': '0.0000000000000000', 'available': '0', 'profile_id':
# 'c6376665-d9a9-48f7-9af9-e99491b91b87', 'trading_enabled': True}, {'id': 'dd5c002b-35fc-4c4b-b2a2-0bbe2312215c',
# 'currency': 'UMA', 'balance': '0.0000000000000000', 'hold': '0.0000000000000000', 'available': '0', 'profile_id':
# 'c6376665-d9a9-48f7-9af9-e99491b91b87', 'trading_enabled': True}, {'id': 'a9d23970-1326-4be2-b5c3-f2029a6b74d8',
# 'currency': 'UNI', 'balance': '0.0000000000000000', 'hold': '0.0000000000000000', 'available': '0', 'profile_id':
# 'c6376665-d9a9-48f7-9af9-e99491b91b87', 'trading_enabled': True}, {'id': 'd8a6b3ee-1063-470c-aa8f-14bef579e7e6',
# 'currency': 'USD', 'balance': '110.7443807978623000', 'hold': '91.2996250000000000', 'available':
# '19.4447557978623', 'profile_id': 'c6376665-d9a9-48f7-9af9-e99491b91b87', 'trading_enabled': True},
# {'id': '1f8612c0-8bba-438b-b004-3d7e9732ab67', 'currency': 'USDC', 'balance': '0.0000000000000000',
# 'hold': '0.0000000000000000', 'available': '0', 'profile_id': 'c6376665-d9a9-48f7-9af9-e99491b91b87',
# 'trading_enabled': True}, {'id': '4ae1c95d-cea1-48fb-973b-204bb9232278', 'currency': 'USDT', 'balance':
# '8.9000000000000000', 'hold': '0.0000000000000000', 'available': '8.9', 'profile_id':
# 'c6376665-d9a9-48f7-9af9-e99491b91b87', 'trading_enabled': True}, {'id': 'd0e2978e-7a94-4326-9062-2b7e29a05b78',
# 'currency': 'WBTC', 'balance': '0.0000000000000000', 'hold': '0.0000000000000000', 'available': '0', 'profile_id':
# 'c6376665-d9a9-48f7-9af9-e99491b91b87', 'trading_enabled': True}, {'id': 'c036c87f-138c-41d3-907f-d657a3237b74',
# 'currency': 'XLM', 'balance': '0.0000000000000000', 'hold': '0.0000000000000000', 'available': '0', 'profile_id':
# 'c6376665-d9a9-48f7-9af9-e99491b91b87', 'trading_enabled': True}, {'id': '7be53f2f-8e2d-4c7f-9629-f6f9edeaae4c',
# 'currency': 'XRP', 'balance': '0.0000000000000000', 'hold': '0.0000000000000000', 'available': '0', 'profile_id':
# 'c6376665-d9a9-48f7-9af9-e99491b91b87', 'trading_enabled': True}, {'id': '2db4fd2f-04b3-46e4-9434-d618296a5bc1',
# 'currency': 'XTZ', 'balance': '4.5800000000000000', 'hold': '0.0000000000000000', 'available': '4.58',
# 'profile_id': 'c6376665-d9a9-48f7-9af9-e99491b91b87', 'trading_enabled': True},
# {'id': '253ebd6a-371c-470a-a931-a92110fb6299', 'currency': 'YFI', 'balance': '0.0000000000000000',
# 'hold': '0.0000000000000000', 'available': '0', 'profile_id': 'c6376665-d9a9-48f7-9af9-e99491b91b87',
# 'trading_enabled': True}, {'id': '75df8b80-4a4f-47c2-99ad-60ae63afb926', 'currency': 'ZEC', 'balance':
# '0.0000000000000000', 'hold': '0.0000000000000000', 'available': '0', 'profile_id':
# 'c6376665-d9a9-48f7-9af9-e99491b91b87', 'trading_enabled': True}, {'id': 'b71a50ff-d0cc-443a-858d-e59d9404c4fc',
# 'currency': 'ZRX', 'balance': '0.0000000000000000', 'hold': '0.0000000000000000', 'available': '0', 'profile_id':
# 'c6376665-d9a9-48f7-9af9-e99491b91b87', 'trading_enabled': True}]

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
