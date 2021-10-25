from imports import *


def futures_buy(config, client):
    client.futures_create_order(symbol='DOGEUSDT', type='MARKET', side='BUY', quantity=100)
