from imports import *


def update_binance_account_futures_config(client, config_tradoge):
    for position in client.futures_account()['positions']:
        if position['symbol'] == f"DOGE{config_tradoge['futures_trading_pair']}":
            if (position['isolated'] and config_tradoge['futures_margin_mode'] != "Isolated") or (
                    not position['isolated'] and config_tradoge['futures_margin_mode'] != "Crossed"):
                client.futures_change_margin_type(symbol=f"DOGE{config_tradoge['futures_trading_pair']}",
                                                  marginType=config_tradoge['futures_margin_mode'].upper())
            print(position)

    client.futures_change_leverage(symbol=f"DOGE{config_tradoge['futures_trading_pair']}",
                                   leverage=config_tradoge['futures_leverage'])


def spot_buy(client, config, total):
    try:
        # Buy order

        buy = client.order_market_buy(
            symbol='DOGE' + config['tradoge']['spot_trading_pair'],
            quantity=total,
        )

        # Use limit order instead with a different price to test
        '''
        buy = client.order_limit_buy(
            symbol='DOGE'+ config['tradoge']['spot_trading_pair'],
            quantity=total,
            price='0.03'
        )
        '''
        return buy
    except Exception as e:
        restart_on_error(e, 60)

    # time.sleep(int(answers['sell_delay'])*60)
    reduce_amount = 0


def futures_buy(client, config, total):
    config_tradoge = config['tradoge']
    update_binance_account_futures_config(client, config_tradoge)
    buy = client.futures_create_order(symbol=f"DOGE{config_tradoge['futures_trading_pair']}", type='MARKET', side='BUY',
                                quantity=total)
    # client.futures_change_margin_type(symbol='DOGEUSDT', marginType='ISOLATED')
    # client.futures_change_leverage(symbol='DOGEUSDT', leverage=2)
    return buy

def futures_sell(client, config, total):
    config_tradoge = config['tradoge']
    sell = client.futures_create_order(symbol=f"DOGE{config_tradoge['futures_trading_pair']}", type='MARKET', side='SELL',
                                quantity=total)
    return sell


def futures_trailing_stop_loss(client, config, total, callbackRate):
    config_tradoge = config['tradoge']
    trailing = client.futures_create_order(symbol="BTCUSDT",
                                           type="TRAILING_STOP_MARKET",
                                           callbackRate=callbackRate,
                                           side='SELL',
                                           quantity=total,
                                           # activationPrice=price * 1.01,
                                           reduceOnly='true')
    return trailing
