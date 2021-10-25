import ccxt
from pprint import pprint


def table(values):
    first = values[0]
    keys = list(first.keys()) if isinstance(first, dict) else range(0, len(first))
    widths = [max([len(str(v[k])) for v in values]) for k in keys]
    string = ' | '.join(['{:<' + str(w) + '}' for w in widths])
    return "\n".join([string.format(*[str(v[k]) for k in keys]) for v in values])


print(ccxt.exchanges)
ccxtbinance = ccxt.binance(
    {
        'apiKey': 'old',
        'secret': 'old',
        'enableRateLimit': True,
        'options': {
            'defaultType': 'future',
        }
    }
)
ccxtbinance.set_sandbox_mode(True)

print('Fetching your balance:')
response = ccxtbinance.fetch_balance()
pprint(response['total'])

print('----------------------------------------------------------------------')
markets = ccxtbinance.load_markets()


symbol = 'DOGE/USDT'
market = ccxtbinance.market(symbol)
leverage = 25
print("risk :")
response = ccxtbinance.fapiPrivateGetPositionRisk()


for res in response:
    if res['symbol'] == "BTCUSDT":
        print(res)

print('----------------------------------------------------------------------')

response = ccxtbinance.fapiPrivate_post_leverage({
    'symbol': market['id'],
    'leverage': leverage,
})

print(response)

# print('----------------------------------------------------------------------')
# print(market['id'])
# response = ccxtbinance.fapiPrivate_post_margintype({
#     'symbol': market['id'],
#     'marginType': 'ISOLATED',
# })
print('----------------------------------------------------------------------')

# response = ccxtbinance.fapiPrivate_post_positionmargin({
#     'symbol': market['id'],
#     'amount': 1000,  # ←-------------- YOUR AMOUNT HERE
#     'positionSide': 'LONG',  # use BOTH for One-way positions, LONG or SHORT for Hedge Mode
#     'type': 1,  # 1 = add position margin, 2 = reduce position margin
# })
# response = ccxtbinance.create_order(symbol= symbol, type= "MARKET", amount= 1000, side= 'BUY')
# response = ccxtbinance.create_order(symbol= symbol, type = 'stop_loss_limit', amount= 1000, side= 'BUY', params ={'stopPrice': 0.3} )
# print(response)

import random
if (ccxtbinance.has['fetchTicker']):
    print(ccxtbinance.fetch_ticker('DOGE/USDT')) # ticker for LTC/ZEC
    symbols = list(ccxtbinance.markets.keys())
    print(ccxtbinance.fetch_ticker(random.choice(symbols)))