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
    import threading
    from colorama import init, Fore, Back, Style
except:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])


try:
    import twint
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--user", "--upgrade","git+https://github.com/twintproject/twint.git@origin/master#egg=twint"])
    import twint

init(convert=True)

# Colors class for tuning CLI
class colors:
    reset='\033[0m'
    class fg: 
        black='\033[30m'
        red='\033[31m'
        green='\033[32m'
        orange='\033[33m'
        blue='\033[34m'
        purple='\033[35m'
        cyan='\033[36m'
        lightgrey='\033[37m'
        darkgrey='\033[90m'
        lightred='\033[91m'
        lightgreen='\033[92m'
        yellow='\033[93m'
        lightblue='\033[94m'
        pink='\033[95m'
        lightcyan = '\033[96m'

# Config class for retrieving Binance credentials from .toml file
class Config:
    def __init__(self):
        self.config = toml.load('config.toml')
        if self.config["binance"]:
            binance = self.config["binance"]
            self.api_key = binance["api_key"]
            self.secret_key = binance["secret_key"]
    
    def get_toml(self):
        self.config = toml.load('config.toml')
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

def on_start():
    # TODO import : pip3 install --user --upgrade git+https://github.com/twintproject/twint.git@origin/master#egg=twint
    # Decorations
    print(Fore.YELLOW)
    obj = timg.Renderer()                                                                                               
    obj.load_image_from_file("dogecoin.png")                                                                                
    obj.resize(100,100)
    obj.render(timg.ASCIIMethod)
    tprint("TraDOGE","font: varsity")
    print(Fore.RESET)


def print_avg_price(client):
    get = client.get_avg_price(symbol='DOGEUSDT')
    print('Average price of DOGE in USD for the last '+ str(get['mins']) + ' minutes : \n' + Fore.YELLOW + str(get['price']) + " $" + Fore.RESET)

def setup(config, client):
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
        },
        {
            'type': 'input',
            'name': 'quantity',
            'message': 'How many DOGE coins do you want to buy when Elon tweets ?',
        },
        {
            'type': 'input',
            'name': 'sell_delay',
            'message': 'After how many minutes do you want to sell ? 5min is recommended.',
        },
    ]
    print_avg_price(client)
    answers = prompt(setup_questions)
    if not (bool(answers['tweet_frequency']) & bool(answers['trading_pair']) & bool(answers['quantity']) & bool(answers['sell_delay'])):
        sys.exit("Security Stop : Empty input")
    file_name='config.toml'
    data = toml.load(file_name)
    data['tradoge']=answers
    with open(file_name, "w") as toml_file:
        toml.dump(data, toml_file)
    menu(config, client)

def menu(nconfig, client):
    on_start()
    config = nconfig.get_toml()
    doge_balance = client.get_asset_balance(asset='DOGE')['free']
    pair_balance = client.get_asset_balance(asset=config['tradoge']['trading_pair'])['free']
    print("\033[1m"+'❯ Current account balance : '+"\033[0m")
    print(Fore.YELLOW + str(doge_balance) + ' DOGE' + Fore.RESET)
    print(Fore.YELLOW + str(pair_balance) + ' '+ config['tradoge']['trading_pair'] + Fore.RESET)
    print_avg_price(client)
    price = client.get_avg_price(symbol='DOGEUSDT')['price']
    doge_value = float(doge_balance) * float(price)
    print('DOGE account average value : \n' + Fore.YELLOW + str(round(doge_value, 2)) + ' $' + Fore.RESET)
    print('')
    print("\033[1m"+'❯ Current configuration : '+"\033[0m")
    print('Tweets update frequency : \n' + Fore.YELLOW + config['tradoge']['tweet_frequency'] + ' seconds'+Fore.RESET)
    print('Trading pair : \n' + Fore.YELLOW + 'DOGE/'+config['tradoge']['trading_pair'] +Fore.RESET)
    print('Quantity of DOGE coins to buy & sell : \n' + Fore.YELLOW + config['tradoge']['quantity'] + ' DOGE'+Fore.RESET)
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
        setup(nconfig, client)
    elif menu_answers['start'] == 'Exit':
        sys.exit("User exited from TraDOGE")


def signup():
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
        print(colors.fg.red+'Passwords are not the same, try again'+Fore.RESET)

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
            print(colors.fg.red + 'PASSWORD IS WRONG. Try again \n' + Fore.RESET)
            time.sleep(1)
            print('Type RESET to change your API keys')
            time.sleep(1)
            continue
        client=Client(api_key, secret_key)
        if client.get_system_status()['status'] == 0:
            print(colors.fg.green + 'CONNECTED TO YOUR BINANCE ACCOUNT' + Fore.RESET)
            time.sleep(1)
            break
        else:
            print(colors.fg.red + 'Connection to your Binance account failed. \n' + Fore.RESET)
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
                sys.exit("User exited from TraDOGE")
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

    file_name='config.toml'
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
    new_config = Config()
    config = new_config.get_toml()
    if config['binance']['secret_key'] and config['binance']['secret_key']:
        client=login(new_config)
    else:
        client=signup()
    #client = Client(config.api_key, config.secret_key)
    menu(new_config, client)
    config = Config()
    config = config.get_toml()

    # Declarations
    tweets = []

    c = twint.Config()
    c.Username = "elonmusk"
    c.Search = "doge OR dogecoin"
    c.Limit = 5
    c.Store_object = True
    c.Store_object_tweets_list = tweets
    c.Hide_output = True
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

        elif tweet_datetime>lastTweet_datetime and '@' not in tweets[0].tweet:
            print("NEW TWEET")
            print(tweets[0].tweet)
            
            # Buy order
            #'''
            buy = client.order_market_buy(
                symbol='DOGE'+ config['tradoge']['trading_pair'],
                quantity=int(config['tradoge']['quantity']),
            )
            # Use limit order instead with a different price to test
            '''
            buy = client.order_limit_buy(
                symbol='DOGE'+ config['tradoge']['trading_pair'],
                quantity=int(config['tradoge']['quantity']),
                price='0.04'
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
                quantity=int(config['tradoge']['quantity']),
            )
            # Use limit order instead with a different price to test
            '''
            sell = client.order_limit_sell(
                symbol='DOGE'+ config['tradoge']['trading_pair'],
                quantity=int(config['tradoge']['quantity']),
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