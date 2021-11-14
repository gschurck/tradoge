from imports import *


def spot_buy(client, config, total):
    try:
        # Buy order

        buy = client.order_market_buy(
            symbol='DOGE' + config['tradoge']['spot_trading_pair'],
            quantity=total,
        )

        price = float(client.get_symbol_ticker(symbol='DOGEUSDT')['price'])
        # Use limit order instead with a different price to test
        '''
        buy = client.order_limit_buy(
            symbol='DOGE'+ config['tradoge']['spot_trading_pair'],
            quantity=total,
            price='0.03'
        )
        '''
        return price
    except Exception as e:
        restart_on_error(e, 60)

    # time.sleep(int(answers['sell_delay'])*60)
    reduce_amount = 0


def futures_buy(client, config, total):
    config_tradoge = config['tradoge']
    update_binance_account_futures_config(client, config_tradoge)
    client.futures_create_order(symbol=f"DOGE{config_tradoge['futures_trading_pair']}", type='MARKET', side='BUY',
                                quantity=total)
    # client.futures_change_margin_type(symbol='DOGEUSDT', marginType='ISOLATED')
    # client.futures_change_leverage(symbol='DOGEUSDT', leverage=2)


def futures_sell(client, config, total):
    config_tradoge = config['tradoge']
    client.futures_create_order(symbol=f"DOGE{config_tradoge['futures_trading_pair']}", type='MARKET', side='SELL',
                                quantity=total)


def futures_trailing_stop_loss(client, config, total):
    config_tradoge = config['tradoge']
    client.futures_create_order("BTCUSDT",
                                type="TRAILING_STOP_MARKET",
                                callbackRate=1,
                                side='SELL',
                                quantity=total,
                                #activationPrice=price * 1.01,
                                reduceOnly='true')
