# -*- coding: utf-8 -*-
# Developed by Guillaume Schurck : https://github.com/gschurck
# TraDOGE v1.2

print('Check dependencies...')
import sys, subprocess

try:
    import base64
    import os
    from cryptography.fernet import Fernet
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    import time
    import timg
    import toml
    from art import tprint
    from binance.client import Client
    from PyInquirer import prompt
    from progress.bar import Bar
    from datetime import datetime
    from colorama import init, Fore, Back
    import threading
    import requests
except:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])


try:
    import twint
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--user", "--upgrade","git+https://github.com/twintproject/twint.git@origin/master#egg=twint"])
    import twint

init(convert=True)

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

class SlowBar(Bar):
    suffix = Fore.YELLOW + '%(remaining_minutes)d minutes '+ Fore.RESET +' (%(remaining_seconds)d seconds)'
    fill=Fore.YELLOW + '$' + Fore.RESET
    @property
    def remaining_minutes(self):
        return self.eta // 60
    @property
    def remaining_seconds(self):
        return self.eta // 1


def check_updates():
    response = requests.get("https://api.github.com/repos/gschurck/tradoge/releases/latest")
    tag_name=response.json()["tag_name"]
    if tag_name != 'v1.2':
        print(Back.BLUE + 'NEW UPDATE : ' + tag_name +Back.RESET)
        print(Fore.BLUE + 'Please install new version of TraDOGE ' + tag_name)
        print('Follow this link : https://github.com/gschurck/tradoge/releases/latest \n' + Fore.RESET)

        body=response.json()["body"].partition('---')[0]
        print(Fore.YELLOW+'New features : \n' + Fore.RESET + body +'\n\n')
    else:
        print(Fore.GREEN+'TraDOGE is up to date : '+tag_name+Fore.RESET+'\n')

def on_start():
    # Decorations
    print(Fore.YELLOW)
    obj = timg.Renderer()                                                                                               
    obj.load_image_from_file("data/dogecoin.png")                                                                                
    obj.resize(100,100)
    obj.render(timg.ASCIIMethod)
    tprint("TraDOGE","font: varsity")
    print(Fore.RESET)


def print_last_price(client):
    get = client.get_symbol_ticker(symbol="DOGEUSDT")
    print('Current DOGE price : \n' + Fore.YELLOW + str(get['price']) + " $" + Fore.RESET)

def config_error(config, client):
    print(Fore.RED + 'CONFIG ERROR' + Fore.RESET)
    setup(config,client)

def setup(config_obj, client):
    print('Choose your configuration')
    setup_questions = [
        {
            'type': 'input',
            'name': 'tweet_frequency',
            'message': 'At what frequency do you want to check if there is a new tweet from Elon Musk ? (seconds)',
        },
        {
            'type': 'list',
            'name': 'trading_pair',
            'message': 'Which trading pair do you want to use ? DOGE/',
            'choices': [
                'USDT',
                'BUSD',
                'BTC',
                'EUR',
            ]
        }
    ]
    setup_questions_buying_mode = [
            {
            'type': 'list',
            'name': 'buying_mode',
            'message': 'How do you want to buy ?',
            'choices': [
                'Buy DOGE with a fixed dollar amount',
                'Buy a fixed DOGE amount',
            ]
        }
    ]
    setup_questions_USD = [
        {
            'type': 'input',
            'name': 'quantity',
            'message': 'How many dollars do you want to spend on DOGE when Elon tweets about it ? It can be a little less depending on the price but never more. (Enter an integer)',
        },
        {
            'type': 'input',
            'name': 'sell_delay',
            'message': 'After how many minutes do you want to sell ? 5min is recommended.',
        }
    ]
    setup_questions_DOGE = [
        {
            'type': 'input',
            'name': 'quantity',
            'message': 'How many DOGE coins do you want to buy when Elon tweets about it ?',
        },
        {
            'type': 'input',
            'name': 'sell_delay',
            'message': 'After how many minutes do you want to sell ? 5min is recommended.',
        }
    ]
    print_last_price(client)
    file_name='data/config.toml'
    data = toml.load(file_name)
    answers = prompt(setup_questions)
    if answers['trading_pair'] == 'USDT' or answers['trading_pair'] == 'BUSD':
        answers_mode=prompt(setup_questions_buying_mode)
        if answers_mode['buying_mode'] == 'Buy DOGE with a fixed dollar amount':
            answers['buying_mode'] = 'USD'
            answers2 = prompt(setup_questions_USD)
        elif answers_mode['buying_mode'] == 'Buy a fixed DOGE amount':
            answers['buying_mode'] = 'DOGE'
            answers2 = prompt(setup_questions_DOGE)
    else:
        answers['buying_mode'] = 'DOGE'
        answers2 = prompt(setup_questions_DOGE)
    if not (bool(answers['tweet_frequency']) & bool(answers['trading_pair']) & bool(answers2['quantity']) & bool(answers2['sell_delay'])):
        config_error(config_obj, client)
    answers.update(answers2)
    data['tradoge'].update(answers)
    with open(file_name, "w") as toml_file:
        toml.dump(data, toml_file)
    menu(config_obj, client)

def menu(config_obj, client):
    on_start()
    config = config_obj.get_toml()
    doge_balance = client.get_asset_balance(asset='DOGE')['free']
    pair_balance = client.get_asset_balance(asset=config['tradoge']['trading_pair'])['free']
    print("\033[1m"+'> Current account balance : '+"\033[0m")
    print(Fore.YELLOW + str(doge_balance) + ' DOGE' + Fore.RESET)
    print(Fore.YELLOW + str(pair_balance) + ' '+ config['tradoge']['trading_pair'] + Fore.RESET)
    print_last_price(client)
    price = float(client.get_symbol_ticker(symbol='DOGEUSDT')['price'])
    doge_value = float(doge_balance) * float(price)
    doge_buy_value = round(int(config['tradoge']['quantity']) * float(price),2)
    
    print('DOGE account average value : \n' + Fore.YELLOW + str(round(doge_value, 2)) + ' $' + Fore.RESET)
    print('')
    print("\033[1m"+'> Current configuration : '+"\033[0m")
    print('Tweets update frequency : \n' + Fore.YELLOW + config['tradoge']['tweet_frequency'] + ' seconds'+Fore.RESET)
    print('Trading pair : \n' + Fore.YELLOW + 'DOGE/' + config['tradoge']['trading_pair'] + Fore.RESET)
    try:
        if config['tradoge']['buying_mode'] == 'USD':
            print('Amount to spend in dollars : \n' + Fore.YELLOW + config['tradoge']['quantity'] + ' $' + Fore.RESET)
            if getattr( sys, 'frozen', False ):
                # running in a bundle
                print(Fore.YELLOW + config['tradoge']['quantity'] + ' $ = ' + str(doge_buyable_amount(config_obj, client)) + ' DOGE' + Fore.RESET)
            else:
                # running live
                print(Fore.YELLOW + config['tradoge']['quantity'] + ' $ ≃ ' + str(doge_buyable_amount(config_obj, client)) + ' DOGE' + Fore.RESET)
        elif config['tradoge']['buying_mode'] == 'DOGE':
            print('Quantity of DOGE coins to buy & sell : \n' + Fore.YELLOW + config['tradoge']['quantity'] + ' DOGE' + Fore.RESET)
            if getattr(sys, 'frozen', False):
                # running in a bundle
                print(Fore.YELLOW + config['tradoge']['quantity'] + ' DOGE = ' + str(doge_buy_value) + ' $' + Fore.RESET)
            else:
                # running live
                print(Fore.YELLOW + config['tradoge']['quantity'] + ' DOGE ≃ ' + str(doge_buy_value) + ' $' + Fore.RESET)
        else:
            config_error(config_obj, client)
    except KeyError:
        config_error(config_obj,client)
    print('Delay before selling : \n' + Fore.YELLOW + config['tradoge']['sell_delay'] + ' mins'+Fore.RESET)
    print('')

    menu_questions = [
        {
            'type': 'list',
            'name': 'start',
            'message': 'Menu',
            'choices': ['Change config','Start TraDOGE','Exit'],
        },
    ]
    menu_answers=prompt(menu_questions)
    if menu_answers['start'] == 'Change config':
        setup(config_obj, client)
    elif menu_answers['start'] == 'Exit':
        sys.exit("You have quit TraDOGE")

def doge_buyable_amount(config_obj, client):
    config = config_obj.get_toml()
    price = float(client.get_symbol_ticker(symbol='DOGEUSDT')['price'])
    quantity = int(config['tradoge']['quantity'])
    amount = int(quantity // price)
    return amount

def signup():
    check_updates()
    print('Welcome in TraDOGE !')
    while(True):
        ask_passwords = [
            {
                'type': 'password',
                'message': 'Enter a password to encrypt your Binance API secret key :',
                'name': 'password1'
            },
            {
                'type': 'password',
                'message': 'Confirm your password',
                'name': 'password2'
            }
        ]

        passwords = prompt(ask_passwords)
        if passwords['password1'] == passwords['password2']:
            break
        print(Fore.RED+'Passwords are not the same, try again'+Fore.RESET)

    ask_api_keys = [
            {
                'type': 'password',
                'message': 'Paste your Binance API key',
                'name': 'api_key'
            },
            {
                'type': 'password',
                'message': 'Paste your Binance secret key',
                'name': 'secret_key'
            }
        ]
    api_keys = prompt(ask_api_keys)
    api_key = api_keys['api_key']
    secret_key = api_keys['secret_key']
    encrypt_keys(api_key,secret_key , passwords['password1'])
    print("Your keys are encrypted using SHA-256 and stored in config.toml file \nDon't forget your password or you will need to create new API keys")
    time.sleep(3)
    return Client(api_keys['api_key'], api_keys['secret_key'])

def login(config):
    check_updates()
    print('Your Binance API keys are present in config file')
    while(True):
        ask_password = [
            {
                'type': 'password',
                'message': 'Enter your password to decrypt your Binance API keys',
                'name': 'password'
            }
        ]
        password = prompt(ask_password)
        if password['password'] == 'RESET':
            client = signup()
            break;
        try:
            api_key, secret_key = decrypt_keys(config, password['password'])
        except:
            print(Fore.RED + 'PASSWORD IS WRONG. Try again \n' + Fore.RESET)
            time.sleep(1)
            print('Type RESET to change your API keys')
            time.sleep(1)
            continue
        client=Client(api_key, secret_key)
        if client.get_system_status()['status'] == 0:
            print(Fore.GREEN + 'CONNECTED TO YOUR BINANCE ACCOUNT' + Fore.RESET)
            time.sleep(1)
            break
        else:
            print(Fore.RED + 'Connection to your Binance account failed. \n' + Fore.RESET)
            ask_retry = [
                {
                    'type': 'list',
                    'message': 'What do you want to do ?',
                    'name': 'retry',
                    'choices': ['Retry password','Setup new API keys','Exit']
                }
            ]
            retry = prompt(ask_retry)
            if retry['retry'] == 'Setup new API keys':
                client = signup()
            elif retry['retry'] == 'Exit':
                sys.exit("You have quit TraDOGE")
    return client

def encrypt_keys(api_key, secret_key, password):
    password = password.encode()
    salt = os.urandom(16)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password))
    f = Fernet(key)
    api_token = f.encrypt(api_key.encode())
    secret_token = f.encrypt(secret_key.encode())

    file_name='data/config.toml'
    data = toml.load(file_name)
    data['binance']['api_key']=api_token
    data['binance']['secret_key']=secret_token
    data['binance']['salt']=salt
    with open(file_name, "w") as toml_file:
        toml.dump(data, toml_file)

def decrypt_keys(config, password):
    config=config.get_toml()
    password = password.encode()
    salt = bytes(config['binance']['salt'])
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password))
    f = Fernet(key)
    api_token = bytes(config['binance']['api_key'])
    secret_token = bytes(config['binance']['secret_key'])

    return f.decrypt(api_token).decode("utf-8"), f.decrypt(secret_token).decode("utf-8")

def check_client(client):
    print(client.ping())

def open_orders(client):
    orders = client.get_open_orders(symbol='BNBBTC')

def waiting():
    while(True):
        print('waiting')
        time.sleep(5)

def main():
    on_start()
    # Binance credentials setup
    config_obj = Config()
    config = config_obj.get_toml()
    if config['binance']['secret_key'] and config['binance']['secret_key']:
        client=login(config_obj)
    else:
        client=signup()
    #client = Client(config.api_key, config.secret_key)
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
    lastTweet = tweets[0]
    lastTweet_datetime = datetime.strptime(tweets[0].datetime[:19], '%Y-%m-%d  %H:%M:%S')
    '''
    w = threading.Thread(target=waiting)
    w.start()
    '''
    while (True):
        tweets.clear()
        twint.run.Search(c)
        tweet_datetime = datetime.strptime(tweets[0].datetime[:19], '%Y-%m-%d  %H:%M:%S')
        if lastTweet.id == tweets[0].id:
            print(datetime.now().strftime("%H:%M:%S")+" : Waiting for new DOGE tweet from Elon  (CTRL+C to stop)", end="\r")
        elif tweet_datetime > lastTweet_datetime and '@' not in tweets[0].tweet:
            if config['tradoge']['buying_mode'] == 'USD':
                total = doge_buyable_amount(config_obj, client)
            else:
                total = int(config['tradoge']['quantity'])

            print("NEW TWEET")
            print(tweets[0].tweet)
            
            # Buy order
            #'''
            buy = client.order_market_buy(
                symbol = 'DOGE'+ config['tradoge']['trading_pair'],
                quantity = total,
            )
            # Use limit order instead with a different price to test
            '''
            buy = client.order_limit_buy(
                symbol='DOGE'+ config['tradoge']['trading_pair'],
                quantity=total,
                price='0.03'
            )
            '''
            print(buy)
            print("ACHAT EFFECTUE")
            
            # Waiting time before selling, with progress bar

            delay_seconds=int(config['tradoge']['sell_delay'])*60
            bar = SlowBar('Waiting to sell ' + config['tradoge']['quantity'] + ' DOGE in '+ config['tradoge']['trading_pair'], max=delay_seconds)
            for i in reversed(range(delay_seconds)):
                time.sleep(1)
                bar.next()
            bar.finish()
            #time.sleep(int(answers['sell_delay'])*60)

            # Sell order
            #'''
            sell = client.order_market_sell(
                symbol='DOGE'+ config['tradoge']['trading_pair'],
                quantity=total,
            )
            # Use limit order instead with a different price to test
            '''
            sell = client.order_limit_sell(
                symbol='DOGE'+ config['tradoge']['trading_pair'],
                quantity=total,
                price='0.1'
            )
            '''
            print(sell)
            print('Sold')
            print('\n')

        # Check new tweet every x seconds
        time.sleep(int(config['tradoge']['tweet_frequency']))
        lastTweet = tweets[0]
        lastTweet_datetime=tweet_datetime


if __name__ == "__main__":
    main()