def get_binance_balance(api_key, api_secret):
    """
    Get the current balance of the Binance account
    :param api_key:
    :param api_secret:
    :return:
    """
    # Create Binance client
    client = Client(api_key, api_secret)

    # Get current balance
    balance = client.get_account()

    # Print the balance
    print(balance)