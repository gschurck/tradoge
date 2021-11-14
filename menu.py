from imports import *


def check_updates():
    response = requests.get("https://api.github.com/repos/gschurck/tradoge/releases/latest")
    tag_name = response.json()["tag_name"]
    if tag_name != version:
        print(Back.BLUE + 'NEW UPDATE : ' + tag_name + Back.RESET)
        print(Fore.BLUE + 'Please install new version of TraDOGE ' + tag_name)
        print('Follow this link : https://github.com/gschurck/tradoge/releases/latest \n' + Fore.RESET)

        body = response.json()["body"].partition('---')[0]
        print(Fore.YELLOW + 'Changelog : \n' + Fore.RESET + body + '\n')
    else:
        print(Fore.GREEN + 'TraDOGE is up to date : ' + tag_name + Fore.RESET + '\n')
    if testMode:
        print(f"{Fore.RED}TESTMODE{Fore.RESET}")


def print_last_price(client):
    get = client.get_symbol_ticker(symbol=DOGEUSDT)
    print('Current DOGE price : \n' + Fore.YELLOW + str(get['price']) + " $" + Fore.RESET)


def config_error(client, config):
    print(Fore.RED + 'CONFIG ERROR' + Fore.RESET)
    setup(client, config)


def doge_buyable_amount(client, config_tradoge):
    price = float(client.get_symbol_ticker(symbol=DOGEUSDT)['price'])
    quantity = int(config_tradoge['quantity'])
    amount = int(quantity // price)
    return amount


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


def setup(client, config):
    config_tradoge = config['tradoge']
    print('Choose your configuration')

    setup_questions = {
        'start': [
            {
                'type': 'input',
                'name': 'tweet_frequency',
                'message': 'At what frequency do you want to check if there is a new tweet from Elon Musk ? (seconds)',
            },
            {
                'type': 'list',
                'name': 'market',
                'message': 'Do you want to trade on Spot or Futures market ?',
                'choices': [
                    'Spot',
                    'Futures',
                ]
            }
        ],
        'spot_trading_pair': {
            'type': 'list',
            'name': 'spot_trading_pair',
            'message': 'Which trading pair do you want to use ? DOGE/',
            'choices': [
                'USDT',
                'BUSD',
                'BTC',
                'EUR',
            ]
        },
        'futures': [
            {
                'type': 'list',
                'name': 'futures_contract_type',
                'message': 'Choose a margin type',
                'choices': [
                    'USDⓈ-M',
                    'COIN-M',
                ]
            },
            {
                'type': 'list',
                'name': 'futures_trading_pair',
                'message': 'Which perpetual contract do you want to use ? DOGE/',
                'choices': [
                    'USDT',
                    'BUSD',
                ]
            },
            {
                'type': 'list',
                'name': 'futures_margin_mode',
                'message': 'Choose a margin mode :',
                'choices': [
                    'Isolated',
                    'Crossed',
                ]
            },
            {
                'type': 'input',
                'name': 'futures_leverage',
                'message': 'Choose the leverage (min: 1, max: 50) :',
            }
        ],
        'setup_questions_buying_mode': [
            {
                'type': 'list',
                'name': 'buying_mode',
                'message': 'How do you want to buy ?',
                'choices': [
                    'Buy DOGE with a fixed dollar amount',
                    'Buy a fixed DOGE amount',
                ]
            }
        ],
        'setup_questions_usd': [
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
        ],
        'setup_questions_btc': [
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
        ],
        'setup_questions_doge': [
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
    }

    for asset in client.futures_account()['assets']:
        if asset['asset'] == "DOGE":
            print(asset)

    def ask_buying_mode():
        answers_mode = prompt(setup_questions['setup_questions_buying_mode'])
        if answers_mode['buying_mode'] == 'Buy DOGE with a fixed dollar amount':
            answers_start['buying_mode'] = 'USD'
            answers2 = prompt(setup_questions['setup_questions_usd'])
        elif answers_mode['buying_mode'] == 'Buy a fixed DOGE amount':
            answers_start['buying_mode'] = 'DOGE'
            answers2 = prompt(setup_questions['setup_questions_doge'])
        return answers2

    print_last_price(client)

    answers_start = prompt(setup_questions['start'])
    if answers_start['market'] == 'Spot':  # SPOT
        answer_trading_pair = prompt(setup_questions['spot_trading_pair'])
        if answers_start['trading_pair'] == 'USDT' or answers_start['trading_pair'] == 'BUSD':
            answers2 = ask_buying_mode()
        else:
            answers_start['buying_mode'] = 'DOGE'
            answers2 = prompt(setup_questions['setup_questions_doge'])

        if not (bool(answers_start['tweet_frequency']) & bool(answers_start['spot_trading_pair']) & bool(
                answers2['quantity']) & bool(answers2['sell_delay'])):
            config_error(client, config)
    elif answers_start['market'] == 'Futures':  # FUTURES
        answer_futures = prompt(setup_questions['futures'])
        print(answer_futures)
        answers2 = ask_buying_mode()

    config_tradoge.update(answers_start) if "answers_start" in locals() else None
    config_tradoge.update(answers2) if "answers2" in locals() else None
    config_tradoge.update(answer_trading_pair) if "answer_trading_pair" in locals() else None
    config_tradoge.update(answer_futures) if "answer_futures" in locals() else None

    save_data(config)

    menu(client, config)


def display_spot_dashboard(client, config):
    config_tradoge = config['tradoge']
    '''
    print(client.get_all_tickers())
    print(client.get_account())
    '''
    # LIVE if else TEST, needed for Binance Testnet
    doge_balance = (client.get_asset_balance(asset='DOGE')['free'] or 0) if (not testMode) else (
            client.get_asset_balance(asset='TRX')['free'] or 0)
    pair_balance = (client.get_asset_balance(asset=config_tradoge['spot_trading_pair'])['free'] or 0) if (
        not testMode) else (client.get_asset_balance(asset='BUSD')['free'] or 0)
    print(f"Market : {config_tradoge['market']}")
    print("\033[1m" + '> Current account balance : ' + "\033[0m")
    print(Fore.YELLOW + str(doge_balance) + ' DOGE' + Fore.RESET)
    print(Fore.YELLOW + str(pair_balance) + ' ' + config_tradoge['spot_trading_pair'] + Fore.RESET)
    print_last_price(client)
    price = float(client.get_symbol_ticker(symbol=DOGEUSDT)['price'])
    doge_value = float(doge_balance) * float(price)
    doge_buy_value = round(int(config_tradoge['quantity']) * float(price), 2)

    print('DOGE account average value : \n' + Fore.YELLOW + str(round(doge_value, 2)) + ' $' + Fore.RESET)
    print('')
    print("\033[1m" + '> Current configuration : ' + "\033[0m")
    print('Tweets update frequency : ' + Fore.YELLOW + config_tradoge['tweet_frequency'] + ' seconds' + Fore.RESET)
    print('Trading pair : ' + Fore.YELLOW + 'DOGE/' + config_tradoge['spot_trading_pair'] + Fore.RESET)
    try:
        if config_tradoge['buying_mode'] == 'USD':
            print('Amount to spend in dollars : \n' + Fore.YELLOW + config_tradoge['quantity'] + ' $' + Fore.RESET)
            if getattr(sys, 'frozen', False):
                # running in a bundle
                print(Fore.YELLOW + config_tradoge['quantity'] + ' $ = ' + str(
                    doge_buyable_amount(client, config_tradoge)) + ' DOGE' + Fore.RESET)
            else:
                # running live
                print(Fore.YELLOW + config_tradoge['quantity'] + ' $ ≃ ' + str(
                    doge_buyable_amount(client, config_tradoge)) + ' DOGE' + Fore.RESET)
        elif config_tradoge['buying_mode'] == 'DOGE':
            print('Quantity of DOGE coins to buy & sell : \n' + Fore.YELLOW + config_tradoge[
                'quantity'] + ' DOGE' + Fore.RESET)
            if getattr(sys, 'frozen', False):
                # running in a bundle
                print(
                    Fore.YELLOW + config_tradoge['quantity'] + ' DOGE = ' + str(doge_buy_value) + ' $' + Fore.RESET)
            else:
                # running live
                print(
                    Fore.YELLOW + config_tradoge['quantity'] + ' DOGE ≃ ' + str(doge_buy_value) + ' $' + Fore.RESET)
        else:
            config_error(client, config)
    except KeyError:
        # TODO FIX probleme affiche deux fois le menu après reconfig
        config_error(client, config)
    print('Delay before selling : \n' + Fore.YELLOW + config_tradoge['sell_delay'] + ' mins' + Fore.RESET)


def display_futures_dashboard(client, config):
    '''
    print(client.futures_create_order(symbol='BTCUSDT', type='MARKET', side='BUY', quantity=1))
    import time
    time.sleep(10)
    futures_trailing_stop_loss(client, config, 1)
    '''
    config_tradoge = config['tradoge']
    pair_balance = 0

    for asset in client.futures_account()['assets']:
        if asset['asset'] == "USDT":
            print(asset)
            pair_balance = asset['walletBalance']

    # LIVE if else TEST, needed for Binance Testnet
    # doge_balance = (client.get_asset_balance(asset='DOGE')['free'] or 0) if (not testMode) else (            client.get_asset_balance(asset='TRX')['free'] or 0)

    # print(client.futures_account(symbol="DOGE"))
    print("\033[1m" + '> Current account balance : ' + "\033[0m")
    # print(Fore.YELLOW + str(doge_balance) + ' DOGE' + Fore.RESET)
    print(Fore.YELLOW + str(pair_balance) + ' ' + config_tradoge['spot_trading_pair'] + Fore.RESET)
    # print_last_price(client)
    price = float(client.futures_symbol_ticker(symbol="DOGEUSDT")['price'])
    print('Current DOGE price : \n' + Fore.YELLOW + str(price) + " $" + Fore.RESET)
    # doge_value = float(doge_balance) * float(price)
    doge_buy_value = round(int(config_tradoge['quantity']) * float(price), 2)

    # print('DOGE account average value : \n' + Fore.YELLOW + str(round(doge_value, 2)) + ' $' + Fore.RESET)
    print('')
    print("\033[1m" + '> Current configuration : ' + "\033[0m")
    print(f"Market : {Fore.YELLOW + config_tradoge['market'] + Fore.RESET}")
    print(f"Contract type : {Fore.YELLOW + config_tradoge['futures_contract_type'] + Fore.RESET}")
    print(f"Margin mode : {Fore.YELLOW + config_tradoge['futures_margin_mode'] + Fore.RESET}\n")
    print('Tweets update frequency : ' + Fore.YELLOW + config_tradoge['tweet_frequency'] + ' seconds' + Fore.RESET)
    print('Trading pair : ' + Fore.YELLOW + 'DOGE/' + config_tradoge['futures_trading_pair'] + Fore.RESET)
    try:
        if config_tradoge['buying_mode'] == 'USD':
            print('Amount to spend in dollars : \n' + Fore.YELLOW + config_tradoge['quantity'] + ' $' + Fore.RESET)
            if getattr(sys, 'frozen', False):
                # running in a bundle
                print(Fore.YELLOW + config_tradoge['quantity'] + ' $ = ' + str(
                    doge_buyable_amount(client, config_tradoge)) + ' DOGE' + Fore.RESET)
            else:
                # running live
                print(Fore.YELLOW + config_tradoge['quantity'] + ' $ ≃ ' + str(
                    doge_buyable_amount(client, config_tradoge)) + ' DOGE' + Fore.RESET)
        elif config_tradoge['buying_mode'] == 'DOGE':
            print('Quantity of DOGE coins to buy & sell : \n' + Fore.YELLOW + config_tradoge[
                'quantity'] + ' DOGE' + Fore.RESET)
            if getattr(sys, 'frozen', False):
                # running in a bundle
                print(
                    Fore.YELLOW + config_tradoge['quantity'] + ' DOGE = ' + str(doge_buy_value) + ' $' + Fore.RESET)
            else:
                # running live
                print(
                    Fore.YELLOW + config_tradoge['quantity'] + ' DOGE ≃ ' + str(doge_buy_value) + ' $' + Fore.RESET)
        else:
            config_error(client, config)
    except KeyError as e:
        # TODO FIX probleme affiche deux fois le menu après reconfig
        print(e)
        config_error(client, config)
    print('Delay before selling : \n' + Fore.YELLOW + config_tradoge['sell_delay'] + ' mins' + Fore.RESET)


def menu(client, config):
    config_tradoge = config['tradoge']
    on_start()
    check_updates()

    if config_tradoge['market'] == "Spot":
        display_spot_dashboard(client, config)
    elif config_tradoge['market'] == "Futures":
        display_futures_dashboard(client, config)

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
        setup(client, config)
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
