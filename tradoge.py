# -*- coding: utf-8 -*-
# Developed by Guillaume Schurck : https://github.com/gschurck

import os
import sys
import time

import logging
import platform
import toml
from colorama import Fore, init

import CONSTANTS
import twitter
import ui
import menu
from CONSTANTS import DOGEUSDT
from trading import process_spot, process_futures, futures_doge_buyable_amount

# colorama
if platform.system() == "Linux":
    init()
else:
    init(convert=True)

logger = logging.getLogger("Error log")
logging.basicConfig(filename="error.log", filemode="w", level=logging.ERROR)


def log_exception(type, value, tb):
    sys.__excepthook__(type, value, tb)
    logger.critical("Fatal error", exc_info=(type, value, tb))


sys.excepthook = log_exception


# Config class for retrieving Binance credentials from .toml file
class Config:
    def __init__(self):
        self.config = toml.load("data/config.toml")
        if "binance" in self.config:
            binance = self.config["binance"]
            self.api_key = binance["api_key"]
            self.secret_key = binance["secret_key"]
        # TODO add key verif

    def get_toml(self):
        self.config = toml.load("data/config.toml")
        if "binance" in self.config:
            binance = self.config["binance"]
            self.api_key = binance["api_key"]
            self.secret_key = binance["secret_key"]
        return self.config


def restart_on_error(exception, seconds):
    print(Fore.RED + "\nERROR :\n" + Fore.RESET)
    print(exception)
    print("\n")
    bar = ui.SlowBar("Restarting the program in ", max=seconds)
    for i in reversed(range(seconds)):
        time.sleep(1)
        bar.next()
    bar.finish()
    print("\n")
    pass


def process_new_tweet(client):
    print("Processing new tweet")
    print(client.futures_symbol_ticker(symbol="BTCUSDT"))
    config_obj = Config()
    config = config_obj.get_toml()
    config_tradoge = config['tradoge']
    print("Config loaded")
    print(config["tradoge"]["market"])
    if config["tradoge"]["market"] == "Spot":
        if config["tradoge"]["buying_mode"] == "USD":
            total = menu.doge_buyable_amount(client=client, config_tradoge=config_tradoge)
            print("Total : " + str(total))
        else:
            total = int(config["tradoge"]["quantity"])
            print("Total2 : " + str(total))
        process_spot(client=client, config=config, total=total)
    elif config["tradoge"]["market"] == "Futures":
        if config["tradoge"]["buying_mode"] == "USD":
            total = futures_doge_buyable_amount(client=client, config_tradoge=config_tradoge)
            print("Total : " + str(total))
        process_futures(client=client, config=config, total=total)


def main():
    print("All dependencies are imported")
    """
    tradoge_stream = twitter.TradogeSearchStream(bearer_token=os.environ["TWITTER_BEARER_TOKEN"], client=None)
    print(twitter.configure_stream_filter_rule(tradoge_stream))
    print(tradoge_stream.get_rules().data[0].value)
    print(tradoge_stream.search_stream())
    """
    ui.on_start()
    # Binance credentials setup
    config_obj = Config()
    config = config_obj.get_toml()
    if config["binance"]["secret_key"] and config["binance"]["secret_key"]:
        client = menu.login(config_obj)
    else:
        client = menu.signup()

    # client = Client(config.api_key, config.secret_key)
    # client.futures_change_margin_type(symbol='DOGEUSDT', marginType='ISOLATED')
    # client.futures_change_leverage(symbol='DOGEUSDT', leverage=2)
    # print(futures_buy(config, client))
    # a=client2.futures_account()
    menu.open_menu(client, config)
    config = config_obj.get_toml()
    config_tradoge = config["tradoge"]
    ping_url = config["twitter"]["ping_url"]

    tradoge_stream = twitter.TradogeSearchStream(
        bearer_token=config['twitter']['bearer_token'],
        client=client,
        ping_url=ping_url
    )
    twitter.configure_stream_filter_rule(tradoge_stream)

    print("Waiting for new DOGE tweet from Elon Musk  (CTRL+C to stop)", end="\n\n")
    twitter.ping_uptime(ping_url, "/start", None)

    while True:
        try:
            print(tradoge_stream.search_stream())
        except Exception as e:
            if CONSTANTS.testMode:
                raise e
            twitter.ping_uptime(ping_url, "/fail", str(e))
            restart_on_error(e, 60)
        """
        if last_tweet.id == tweets[0].id:
            print(datetime.now().strftime("%H:%M:%S") + " : Waiting for new DOGE tweet from Elon  (CTRL+C to stop)",
                  end="\r")
        elif tweet_datetime > last_tweet_datetime and '@' not in tweets[0].tweet:
        """


if __name__ == "__main__":
    main()