from imports import *


def check_updates():
    response = requests.get("https://api.github.com/repos/gschurck/tradoge/releases/latest")
    tag_name = response.json()["tag_name"]
    if tag_name != version:
        print(Back.BLUE + 'NEW UPDATE : ' + tag_name + Back.RESET)
        print(Fore.BLUE + 'Please install new version of TraDOGE ' + tag_name)
        print('Follow this link : https://github.com/gschurck/tradoge/releases/latest \n' + Fore.RESET)

        body = response.json()["body"].partition('---')[0]
        print(Fore.YELLOW + 'New features : \n' + Fore.RESET + body + '\n')
    else:
        print(Fore.GREEN + 'TraDOGE is up to date : ' + tag_name + Fore.RESET + '\n')


def print_last_price(client):
    get = client.get_symbol_ticker(symbol="DOGEUSDT")
    print('Current DOGE price : \n' + Fore.YELLOW + str(get['price']) + " $" + Fore.RESET)


def config_error(config, client):
    print(Fore.RED + 'CONFIG ERROR' + Fore.RESET)
    setup(config, client)


def doge_buyable_amount(config_obj, client):
    config = config_obj.get_toml()
    price = float(client.get_symbol_ticker(symbol='DOGEUSDT')['price'])
    quantity = int(config['tradoge']['quantity'])
    amount = int(quantity // price)
    return amount


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
    setup_questions_usd = [
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
    setup_questions_btc = [
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
    setup_questions_doge = [
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
    file_name = 'data/config.toml'
    data = toml.load(file_name)
    answers = prompt(setup_questions)
    if answers['trading_pair'] == 'USDT' or answers['trading_pair'] == 'BUSD':
        answers_mode = prompt(setup_questions_buying_mode)
        if answers_mode['buying_mode'] == 'Buy DOGE with a fixed dollar amount':
            answers['buying_mode'] = 'USD'
            answers2 = prompt(setup_questions_usd)
        elif answers_mode['buying_mode'] == 'Buy a fixed DOGE amount':
            answers['buying_mode'] = 'DOGE'
            answers2 = prompt(setup_questions_doge)
    else:
        answers['buying_mode'] = 'DOGE'
        answers2 = prompt(setup_questions_doge)
    if not (bool(answers['tweet_frequency']) & bool(answers['trading_pair']) & bool(answers2['quantity']) & bool(
            answers2['sell_delay'])):
        config_error(config_obj, client)
    answers.update(answers2)
    data['tradoge'].update(answers)
    save_data(data)
    menu(config_obj, client)


def menu(config_obj, client):
    on_start()
    check_updates()

    config = config_obj.get_toml()
    doge_balance = 0 if not testMode else client.get_asset_balance(asset='DOGE')['free'] or 0

    pair_balance = 0 if not testMode else client.get_asset_balance(asset=config['tradoge']['trading_pair'])['free'] or 0
    print("\033[1m" + '> Current account balance : ' + "\033[0m")
    print(Fore.YELLOW + str(doge_balance) + ' DOGE' + Fore.RESET)
    print(Fore.YELLOW + str(pair_balance) + ' ' + config['tradoge']['trading_pair'] + Fore.RESET)
    print_last_price(client)
    price = float(client.get_symbol_ticker(symbol='DOGEUSDT')['price'])
    doge_value = float(doge_balance) * float(price)
    doge_buy_value = round(int(config['tradoge']['quantity']) * float(price), 2)

    print('DOGE account average value : \n' + Fore.YELLOW + str(round(doge_value, 2)) + ' $' + Fore.RESET)
    print('')
    print("\033[1m" + '> Current configuration : ' + "\033[0m")
    print('Tweets update frequency : \n' + Fore.YELLOW + config['tradoge']['tweet_frequency'] + ' seconds' + Fore.RESET)
    print('Trading pair : \n' + Fore.YELLOW + 'DOGE/' + config['tradoge']['trading_pair'] + Fore.RESET)
    try:
        if config['tradoge']['buying_mode'] == 'USD':
            print('Amount to spend in dollars : \n' + Fore.YELLOW + config['tradoge']['quantity'] + ' $' + Fore.RESET)
            if getattr(sys, 'frozen', False):
                # running in a bundle
                print(Fore.YELLOW + config['tradoge']['quantity'] + ' $ = ' + str(
                    doge_buyable_amount(config_obj, client)) + ' DOGE' + Fore.RESET)
            else:
                # running live
                print(Fore.YELLOW + config['tradoge']['quantity'] + ' $ ≃ ' + str(
                    doge_buyable_amount(config_obj, client)) + ' DOGE' + Fore.RESET)
        elif config['tradoge']['buying_mode'] == 'DOGE':
            print('Quantity of DOGE coins to buy & sell : \n' + Fore.YELLOW + config['tradoge'][
                'quantity'] + ' DOGE' + Fore.RESET)
            if getattr(sys, 'frozen', False):
                # running in a bundle
                print(
                    Fore.YELLOW + config['tradoge']['quantity'] + ' DOGE = ' + str(doge_buy_value) + ' $' + Fore.RESET)
            else:
                # running live
                print(
                    Fore.YELLOW + config['tradoge']['quantity'] + ' DOGE ≃ ' + str(doge_buy_value) + ' $' + Fore.RESET)
        else:
            config_error(config_obj, client)
    except KeyError:
        # TODO FIX probleme affiche deux fois le menu après reconfig
        config_error(config_obj, client)
    print('Delay before selling : \n' + Fore.YELLOW + config['tradoge']['sell_delay'] + ' mins' + Fore.RESET)
    print('')

    menu_questions = [
        {
            'type': 'list',
            'name': 'start',
            'message': 'Menu',
            'choices': ['Change config', 'Start TraDOGE', 'Exit'],
        },
    ]
    menu_answers = prompt(menu_questions)
    if menu_answers['start'] == 'Change config':
        setup(config_obj, client)
    elif menu_answers['start'] == 'Exit':
        sys.exit("You have quit TraDOGE")


def signup():
    check_updates()
    print('Welcome in TraDOGE !')
    while True:
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
        print(Fore.RED + 'Passwords are not the same, try again' + Fore.RESET)

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
    encrypt_keys(api_key, secret_key, passwords['password1'])
    print(
        "Your keys are encrypted using SHA-256 and stored in config.toml file \nDon't forget your password or you "
        "will need to create new API keys")
    time.sleep(3)
    return Client(api_keys['api_key'], api_keys['secret_key'], testnet=testMode)


def login(config):
    check_updates()
    print('Your Binance API keys are present in config file')
    while True:
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
            break
        try:
            api_key, secret_key = decrypt_keys(config, password['password'])
        except:
            print(Fore.RED + 'PASSWORD IS WRONG. Try again \n' + Fore.RESET)
            time.sleep(1)
            print('Type RESET to change your API keys')
            time.sleep(1)
            continue
        client = Client(api_key, secret_key, testnet=testMode)
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
                    'choices': ['Retry password', 'Setup new API keys', 'Exit']
                }
            ]
            retry = prompt(ask_retry)
            if retry['retry'] == 'Setup new API keys':
                client = signup()
            elif retry['retry'] == 'Exit':
                sys.exit("You have quit TraDOGE")
    return client
