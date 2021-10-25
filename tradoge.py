# -*- coding: utf-8 -*-
# Developed by Guillaume Schurck : https://github.com/gschurck


from imports import *

print("All dependencies are imported")

init(convert=True)

logger = logging.getLogger('Error log')
logging.basicConfig(filename='error.log', filemode='w', level=logging.ERROR)


def log_exception(type, value, tb):
    sys.__excepthook__(type, value, tb)
    logger.critical("Fatal error", exc_info=(type, value, tb))


sys.excepthook = log_exception


# Config class for retrieving Binance credentials from .toml file
class Config:
    def __init__(self):
        self.config = toml.load('data/config.toml')
        if self.config["binance"]:
            binance = self.config["binance"]
            self.api_key = binance["api_key"]
            self.secret_key = binance["secret_key"]

    def get_toml(self):
        self.config = toml.load('data/config.toml')
        binance = self.config["binance"]
        self.api_key = binance["api_key"]
        self.secret_key = binance["secret_key"]
        return self.config


def restart_on_error(exception, seconds):
    print(Fore.RED + '\nERROR :\n' + Fore.RESET)
    print(exception)
    print('\n')
    bar = SlowBar('Restarting the program in ', max=seconds)
    for i in reversed(range(seconds)):
        time.sleep(1)
        bar.next()
    bar.finish()
    print('\n')
    pass


def main():
    on_start()
    # Binance credentials setup
    config_obj = Config()
    config = config_obj.get_toml()
    if config['binance']['secret_key'] and config['binance']['secret_key']:
        client = login(config_obj)
    else:
        client = signup()

    # client = Client(config.api_key, config.secret_key)
    # client.futures_change_margin_type(symbol='DOGEUSDT', marginType='ISOLATED')
    # client.futures_change_leverage(symbol='DOGEUSDT', leverage=2)
    # print(futures_buy(config, client))
    #a=client2.futures_account()
    menu(config_obj, client)
    config = config_obj.get_toml()


    # Declarations
    tweets = []

    c = twint.Config()
    c.Username = "elonmusk"
    c.Search = "doge OR dogecoin"
    c.Limit = 2
    c.Store_object = True
    c.Store_object_tweets_list = tweets
    c.Hide_output = True
    c.Filter_retweets = True
    twint.run.Search(c)
    last_tweet = tweets[0]
    last_tweet_datetime = datetime.strptime(tweets[0].datetime[:19], '%Y-%m-%d  %H:%M:%S')

    while True:
        try:
            tweets.clear()
            twint.run.Search(c)
            tweet_datetime = datetime.strptime(tweets[0].datetime[:19], '%Y-%m-%d  %H:%M:%S')
        except Exception as e:
            restart_on_error(e, 60)

        if last_tweet.id == tweets[0].id:
            print(datetime.now().strftime("%H:%M:%S") + " : Waiting for new DOGE tweet from Elon  (CTRL+C to stop)",
                  end="\r")
        elif tweet_datetime > last_tweet_datetime and '@' not in tweets[0].tweet:
            last_tweet = tweets[0]
            last_tweet_datetime = tweet_datetime

            if config['tradoge']['buying_mode'] == 'USD':
                total = doge_buyable_amount(config_obj, client)
            else:
                total = int(config['tradoge']['quantity'])

            print(Fore.YELLOW + "NEW TWEET" + Fore.RESET)
            print(tweets[0].tweet)

            try:
                # Buy order
                '''
                buy = client.order_market_buy(
                    symbol='DOGE' + config['tradoge']['trading_pair'],
                    quantity=total,
                )
                '''
                price = float(client.get_symbol_ticker(symbol='DOGEUSDT')['price'])
                # Use limit order instead with a different price to test
                '''
                buy = client.order_limit_buy(
                    symbol='DOGE'+ config['tradoge']['trading_pair'],
                    quantity=total,
                    price='0.03'
                )
                '''
                # print(buy)
                print(Fore.GREEN + 'PURCHASE COMPLETED' + Fore.RESET)
                buy_value = price * total
                print(datetime.now().strftime("%H:%M:%S") + ' TraDOGE bought ' + str(
                    total) + ' DOGE ' + 'for a value of ' + str(round(buy_value, 2)) + ' $\n')
            except Exception as e:
                restart_on_error(e, 60)

            # Waiting time before selling, with progress bar
            delay_seconds = int(config['tradoge']['sell_delay']) * 60
            bar = SlowBar('Waiting to sell ' + str(total) + ' DOGE in ' + config['tradoge']['trading_pair'],
                          max=delay_seconds)
            for i in reversed(range(delay_seconds)):
                time.sleep(1)
                bar.next()
            bar.finish()

            # time.sleep(int(answers['sell_delay'])*60)
            reduce_amount = 0

            def sell_doge(sell_total, reduce):
                try:
                    # Sell order
                    sell = client.order_market_sell(
                        symbol='DOGE' + config['tradoge']['trading_pair'],
                        quantity=sell_total,
                    )

                    # Use limit order instead with a different price to test
                    """
                    sell = client.order_limit_sell(
                        symbol='DOGE'+ config['tradoge']['trading_pair'],
                        quantity=total,
                        price='0.1'
                    )
                    """
                except Exception as sellError:
                    # sell less DOGE in case of insufficient balance
                    print(Fore.RED + 'SELL ERROR : \n' + Fore.RESET + str(sellError))
                    print('Retrying to sell with 10 DOGE less...')
                    reduce += 10
                    print('Selling ' + str(total - reduce) + ' DOGE...')
                    time.sleep(1)
                    sell_doge(total - reduce, reduce)

                price = float(client.get_symbol_ticker(symbol='DOGEUSDT')['price'])
                sell_value = price * sell_total
                print(sell)
                print(Fore.GREEN + 'SALE COMPLETED' + Fore.RESET)
                print(datetime.now().strftime("%H:%M:%S") + ' TraDOGE sold ' + str(
                    sell_total) + ' DOGE ' + ' for a value of ' + str(round(sell_value, 2)) + '\n')
                profit = sell_value - buy_value
                print(Fore.GREEN + 'PROFIT : ' + str(round(profit, 2)) + ' $' + Fore.RESET + '\n')

            sell_doge(total, reduce_amount)

        # Check new tweet every x seconds
        time.sleep(int(config['tradoge']['tweet_frequency']))


if __name__ == "__main__":
    main()
