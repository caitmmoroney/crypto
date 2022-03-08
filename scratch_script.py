# Imports
import os
from api import CoinbaseExchangeAuth, PublicCoinbaseAuth
import time

# Environment variables
api_key = os.environ.get("API_KEY")
api_secret = os.environ.get("API_SECRET")
api_passphrase = os.environ.get("API_PASSPHRASE")
api_url = os.environ.get("API_URL")

auth = CoinbaseExchangeAuth(api_key, api_secret, api_passphrase, api_url)
publicAPI = PublicCoinbaseAuth(api_url)
#
# print(f'Products available on Coinbase Pro: {publicAPI.getproducts()}')


def sell_perc_gain(currency: str, perc: float, cost_basis_usd: float, test: bool = True):
    start = time.time()
    current_price = float(publicAPI.getexchangeprice(f'{currency}-USD'))
    currency_qty = cost_basis_usd / current_price

    while True:
        new_price = float(publicAPI.getexchangeprice(f'{currency}-USD'))
        perc_gain = (new_price - current_price) / current_price

        if perc_gain >= perc:
            if test:
                print(f'It took {time.time() - start} seconds to see a price increase of {perc_gain * 100}%')
            # else:
            #     auth.sellorder(product_market=f'{currency}-USD',
            #                    qty=currency_qty,
            #                    price=new_price)
            #     print('Sell order placed.')
            #     print(f'It took {time.time() - start} seconds to see a price increase of {perc * 100}%')

            return new_price * currency_qty
        else:
            time.sleep(10)


def buy_perc_loss(currency: str, perc: float, cost_basis_usd: float, test: bool = True):
    start = time.time()
    current_price = float(publicAPI.getexchangeprice(f'{currency}-USD'))
    currency_qty = cost_basis_usd / current_price

    while True:
        new_price = float(publicAPI.getexchangeprice(f'{currency}-USD'))
        perc_loss = (current_price - new_price) / current_price

        if perc_loss >= perc:
            if test:
                print(f'It took {time.time() - start} seconds to see a price decrease of {perc_loss * 100}%')
            # else:
            #     auth.buyorder(product_market=f'{currency}-USD',
            #                   qty=currency_qty,
            #                   price=new_price)
            #     print(f'Sell order placed.')
            #     print(f'It took {time.time() - start} seconds to see a price decrease of {perc * 100}%')

            return new_price * currency_qty
        else:
            time.sleep(10)


def trade_strategy_v1(currency: str,
                      buy_perc_decrease: float,
                      sell_perc_increase: float,
                      cost_basis: float,
                      n_trades: int = 10,
                      test: bool = True):
    for i in range(n_trades):
        cost_basis = buy_perc_loss(currency=currency,
                                   perc=buy_perc_decrease,
                                   cost_basis_usd=cost_basis,
                                   test=test)
        cost_basis = sell_perc_gain(currency=currency,
                                    perc=sell_perc_increase,
                                    cost_basis_usd=cost_basis,
                                    test=test)


trade_strategy_v1(currency='ETH', buy_perc_decrease=0.0002, sell_perc_increase=0.00015, cost_basis=100.00)
