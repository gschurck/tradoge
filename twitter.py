import os
import time

from colorama import Fore
from pytwitter import StreamApi

import CONSTANTS
import tradoge

TWITTER_USERNAME = "elonmusk" if not CONSTANTS.testMode else "trouvetonmeme"
TWITTER_QUERY = f"doge from:{TWITTER_USERNAME} OR dogecoin from:{TWITTER_USERNAME}"


# TODO remove None
class TradogeSearchStream(StreamApi):
    def __init__(self, bearer_token, client=None):
        super().__init__(bearer_token=bearer_token)
        self.client = client

    def on_tweet(self, tweet):
        print(Fore.YELLOW + "NEW TWEET" + Fore.RESET)
        print(tweet)
        tradoge.process_new_tweet(self.client)


# TODO remove None
def configure_stream_filter_rule(bearer_token, client=None):
    stream_api = TradogeSearchStream(
        bearer_token=os.environ["TWITTER_BEARER_TOKEN"], client=client
    )
    if not stream_filter_rule_is_ok(stream_api):
        print("No Twitter Stream filter rule found. Creating one...")
        set_stream_filter_rule(stream_api)
        time.sleep(2)
        print("Twitter Stream filter rule is created.")
        if not stream_filter_rule_is_ok(stream_api):
            raise Exception(
                f"ERROR: The stream filter rule can not be correctly configured."
            )
    print("Twitter Stream filter rule is correctly configured.")
    return True


def stream_filter_rule_is_ok(stream_api):
    if len(stream_api.get_rules().data) == 0:
        return False
    elif len(stream_api.get_rules().data) > 1:
        raise Exception(
            "ERROR: The number of Twitter Stream filter rules is greater than one. Current rules:\n{} ".format(
                stream_api.get_rules().data)
        )
    elif stream_api.get_rules().data[0].value != TWITTER_QUERY:
        raise Exception(
            "ERROR: The current Twitter Stream filter rule query '{}' does not correspond to the one expected '{}'".format(
                stream_api.get_rules().data[0].value, TWITTER_QUERY)
        )
    else:
        return True


def set_stream_filter_rule(stream_api):
    tradoge_rule = {
        "add": [
            {"value": TWITTER_QUERY, "tag": "TraDOGE"},
        ]
    }
    stream_api.manage_rules(rules=tradoge_rule)
    return stream_filter_rule_is_ok(stream_api)


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