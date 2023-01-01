import time

from colorama import Fore
from datetime import datetime

import ui
import tradoge
from CONSTANTS import DOGEUSDT


def update_binance_account_futures_config(client, config_tradoge):
    for position in client.futures_account()["positions"]:
        if position["symbol"] == f"DOGE{config_tradoge['futures_trading_pair']}":
            if (
                    position["isolated"]
                    and config_tradoge["futures_margin_mode"] != "Isolated"
            ) or (
                    not position["isolated"]
                    and config_tradoge["futures_margin_mode"] != "Crossed"
            ):
                client.futures_change_margin_type(
                    symbol=f"DOGE{config_tradoge['futures_trading_pair']}",
                    marginType=config_tradoge["futures_margin_mode"].upper(),
                )
            print(position)

    client.futures_change_leverage(
        symbol=f"DOGE{config_tradoge['futures_trading_pair']}",
        leverage=config_tradoge["futures_leverage"],
    )


def process_spot_trades(client, config, total):
    config_tradoge = config["tradoge"]
    buy_order = place_spot_buy_order(client, config, total)
    price = float(client.get_symbol_ticker(symbol="DOGEUSDT")["price"])

    # print(buy)
    print(Fore.GREEN + "PURCHASE COMPLETED" + Fore.RESET)
    buy_value = price * total
    print(
        datetime.now().strftime("%H:%M:%S")
        + " TraDOGE bought "
        + str(total)
        + " DOGE "
        + "for a value of "
        + str(round(buy_value, 2))
        + " $\n"
    )

    # Waiting time before selling, with progress bar

    wait(config_tradoge, total, config_tradoge["spot_trading_pair"])
    delay_seconds = int(config["tradoge"]["sell_delay"]) * 60
    bar = ui.SlowBar(
        "Waiting to sell "
        + str(total)
        + " DOGE in "
        + config["tradoge"]["spot_trading_pair"],
        max=delay_seconds,
    )
    for i in reversed(range(delay_seconds)):
        time.sleep(1)
        bar.next()
    bar.finish()

    reduced_amount = 0
    place_spot_sell_order(
        client=client,
        config=config,
        sell_total=total,
        reduced_amount=reduced_amount,
        buy_value=buy_value,
    )


def place_spot_buy_order(client, config, total):
    try:
        # Buy order

        buy_order = client.order_market_buy(
            symbol="DOGE" + config["tradoge"]["spot_trading_pair"],
            quantity=total,
        )

        # Use limit order instead with a different price to test
        """
        buy = client.order_limit_buy(
            symbol='DOGE'+ config['tradoge']['spot_trading_pair'],
            quantity=total,
            price='0.03'
        )
        """
        return buy_order
    except Exception as e:
        tradoge.restart_on_error(e, 60)

    # time.sleep(int(answers['sell_delay'])*60)


def place_spot_sell_order(client, config, sell_total, reduced_amount, buy_value):
    try:
        # Sell order
        sell = client.order_market_sell(
            symbol="DOGE" + config["tradoge"]["spot_trading_pair"],
            quantity=sell_total,
        )

        # Use limit order instead with a different price to test
        """
        sell = client.order_limit_sell(
            symbol='DOGE'+ config['tradoge']['spot_trading_pair'],
            quantity=total,
            price='0.1'
        )
        """
    except Exception as sellError:
        # sell less DOGE in case of insufficient balance
        print(Fore.RED + "SELL ERROR : \n" + Fore.RESET + str(sellError))
        print("Retrying to sell with 10 DOGE less...")
        reduced_amount += 10
        print("Selling " + str(sell_total - reduced_amount) + " DOGE...")
        place_spot_sell_order(
            client, config, sell_total - reduced_amount, reduced_amount, buy_value
        )

    price = float(client.get_symbol_ticker(symbol="DOGEUSDT")["price"])
    sell_value = price * sell_total
    print(sell)
    print(Fore.GREEN + "SALE COMPLETED" + Fore.RESET)
    print(
        datetime.now().strftime("%H:%M:%S")
        + " TraDOGE sold "
        + str(sell_total)
        + " DOGE "
        + " for a value of "
        + str(round(sell_value, 2))
        + "\n"
    )
    profit = sell_value - buy_value
    print(Fore.GREEN + "PROFIT : " + str(round(profit, 2)) + " $" + Fore.RESET + "\n")


def process_futures_trades(client, config, total):
    print("Processing futures...")
    config_tradoge = config["tradoge"]
    buy_order = place_futures_buy_order(client, config, total)
    print(buy_order)
    print(Fore.GREEN + "PURCHASE COMPLETED" + Fore.RESET)
    price = float(client.futures_symbol_ticker(symbol="DOGEUSDT")["price"])
    buy_value = price * total
    print(
        datetime.now().strftime("%H:%M:%S")
        + " TraDOGE bought "
        + str(total)
        + " DOGE "
        + "for a value of "
        + str(round(buy_value, 2))
        + " $\n"
    )
    trailing_stop = float(config_tradoge["futures_trailing_stop"])
    print("trailing stop : " + str(trailing_stop))
    if trailing_stop > 0:
        time.sleep(1)
        print("waiting for trailing stop...")
        place_futures_trailing_stop_loss_order(client, config, total, trailing_stop)
        print("Trailing stop started")
        # TODO for loop to find the position
        print(
            "Liquidation Price : "
            + client.futures_position_information(symbol="DOGE" + config_tradoge['futures_trading_pair'])[0][
                "liquidationPrice"
            ]
        )
        # TODO
        '''
        while float(
                client.futures_position_information(symbol="DOGE" + config_tradoge['futures_trading_pair'])) >= total:

            print("You are still in profit, waiting for % drop")  # TODO
            print(
                "Current PNL : "
                + client.futures_position_information(symbol="DOGE" + config_tradoge['futures_trading_pair'])[0][
                    "unRealizedProfit"
                ]
            )
            print("")
        '''

    else:
        wait(config_tradoge, total, config_tradoge["futures_trading_pair"])
        place_futures_sell_order(client, config, total)


def get_futures_doge_buyable_amount(client, config_tradoge):
    '''
    print("doge buyable amount")
    print(client.futures_symbol_ticker(symbol="DOGEUSDT"))
    '''
    price = float(client.futures_symbol_ticker(symbol="DOGEUSDT")['price'])
    # print("price : " + str(price))
    quantity = int(config_tradoge['quantity'])
    amount = int(quantity // price)
    return amount


def place_futures_buy_order(client, config, total):
    print("Buying")
    config_tradoge = config["tradoge"]
    update_binance_account_futures_config(client, config_tradoge)
    try:
        buy = client.futures_create_order(
            symbol=f"DOGE{config_tradoge['futures_trading_pair']}",
            type="MARKET",
            side="BUY",
            quantity=total,
        )
    except Exception as e:
        print(e)
        raise e
    # client.futures_change_margin_type(symbol='DOGEUSDT', marginType='ISOLATED')
    # client.futures_change_leverage(symbol='DOGEUSDT', leverage=2)
    return buy


def place_futures_sell_order(client, config, total):
    config_tradoge = config["tradoge"]
    try:
        sell_order = client.futures_create_order(
            symbol=f"DOGE{config_tradoge['futures_trading_pair']}",
            type="MARKET",
            side="SELL",
            quantity=total,
        )
    except Exception as e:
        print(e)
        raise e
    return sell_order


def place_futures_trailing_stop_loss_order(client, config, total, callback_rate):
    print("Configuring trailing stop loss... callback rate : " + str(callback_rate) + "%")
    config_tradoge = config["tradoge"]
    trailing_stop_order = client.futures_create_order(
        symbol="DOGEUSDT",
        type="TRAILING_STOP_MARKET",
        callbackRate=callback_rate,
        side="SELL",
        quantity=total,
        reduceOnly="true",
    )
    return trailing_stop_order


def wait(config_tradoge, total, trading_pair):
    print("Waiting...")
    delay_seconds = int(config_tradoge["sell_delay"]) * 60
    ui.print_loading_bar(
        "Waiting to sell " + str(total) + " DOGE in " + trading_pair, delay_seconds
    )