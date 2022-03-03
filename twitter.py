import os
import socket
import time
import urllib
from datetime import datetime

from colorama import Fore
from pytwitter import StreamApi

import CONSTANTS
import tradoge

TWITTER_USERNAME = "elonmusk" if not CONSTANTS.testMode else "trouvetonmeme"
TWITTER_QUERY = f"doge from:{TWITTER_USERNAME} OR dogecoin from:{TWITTER_USERNAME}"


# TODO remove None
class TradogeSearchStream(StreamApi):
    def __init__(self, bearer_token, client, ping_uptime_url, ping_new_tweet_url):
        super().__init__(bearer_token=bearer_token)
        self.client = client
        self.ping_uptime_url = ping_uptime_url
        self.ping_new_tweet_url = ping_new_tweet_url

    def on_tweet(self, tweet):
        if tweet:
            print(Fore.YELLOW + "NEW TWEET" + Fore.RESET)
            print(tweet)
            tradoge.process_new_tweet(self.client)
            if self.ping_new_tweet_url:
                ping_new_tweet(self.ping_new_tweet_url)
        else:
            print("Empty tweet")

    def on_keep_alive(self):
        if self.ping_uptime_url:
            ping_uptime(self.ping_uptime_url, "", None)


# TODO remove None
def configure_stream_filter_rule(twitter_api_stream):
    if not stream_filter_rule_is_ok(twitter_api_stream):
        print("No Twitter Stream filter rule found. Creating one...")
        set_stream_filter_rule(twitter_api_stream)
        time.sleep(2)
        print("Twitter Stream filter rule is created.")
        if not stream_filter_rule_is_ok(twitter_api_stream):
            raise Exception(
                f"ERROR: The stream filter rule can not be correctly configured."
            )
    print("Twitter Stream filter rule is correctly configured.")
    return True


def stream_filter_rule_is_ok(twitter_api_stream):
    if len(twitter_api_stream.get_rules().data) == 0:
        return False
    elif len(twitter_api_stream.get_rules().data) > 1:
        raise Exception(
            "ERROR: The number of Twitter Stream filter rules is greater than one. Current rules:\n{} ".format(
                twitter_api_stream.get_rules().data)
        )
    elif twitter_api_stream.get_rules().data[0].value != TWITTER_QUERY:
        raise Exception(
            "ERROR: The current Twitter Stream filter rule query '{}' does not correspond to the one expected '{}'".format(
                twitter_api_stream.get_rules().data[0].value, TWITTER_QUERY)
        )
    else:
        return True


def set_stream_filter_rule(twitter_api_stream):
    tradoge_rule = {
        "add": [
            {"value": TWITTER_QUERY, "tag": "TraDOGE"},
        ]
    }
    twitter_api_stream.manage_rules(rules=tradoge_rule)
    return stream_filter_rule_is_ok(twitter_api_stream)


def ping_uptime(ping_url, endpoint, message):
    if message:
        data = urllib.parse.urlencode({"message": "TEST MESSAGE"}).encode()
        request = urllib.request.Request(ping_url + endpoint, data=data)
    else:
        request = ping_url + endpoint
    try:
        urllib.request.urlopen(request, timeout=10)
        print("Last Twitter connection check : " + Fore.GREEN + datetime.now().strftime("%H:%M:%S") + Fore.RESET,
              end="\r")
    except socket.error as e:
        # Log ping failure here...
        print("Ping failed: %s" % e)


def ping_new_tweet(ping_url):
    try:
        urllib.request.urlopen(ping_url, timeout=10)
    except socket.error as e:
        # Log ping failure here...
        print("Ping failed: %s" % e)


"""
def start_tradoge():
    try:
        stream_api = SearchStream(bearer_token=os.environ['TWITTER_BEARER_TOKEN'])
    except Exception as e:
        print(Fore.RED + '\nERROR :\n' + Fore.RESET)
        print(e)
        print('\n')
        print("Restarting...")
        start_tradoge()
"""

if __name__ == "__main__":
    stream_api = TradogeSearchStream(bearer_token=os.environ['TWITTER_BEARER_TOKEN'])

    """
    api = Api(bearer_token=os.environ['TWITTER_BEARER_TOKEN'])
    print(api.get_users(usernames="elonmusk"))
  
    print(stream_api.get_rules())
    # stream_api.filter(track=['elonmusk'])
    """
    r = {
        "add": [
            {"value": "doges from:trouvetonmeme OR dogecoin from:trouvetonmeme", "tag": "doge test ttm"},
        ]
    }
    # stream_api.manage_rules(rules=r)
    """
    stream_api.manage_rules(
        rules={"delete": {"ids": ["1492655084647469058", "1492864338172039171", "1492866964632526850"]}})
    """
    print(stream_api.get_rules())
    print(stream_api.search_stream())