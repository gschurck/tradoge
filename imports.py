import subprocess
import sys
import base64
import time
import os

print('Check dependencies...')

try:
    print("Importing packages...")
    from cryptography.fernet import Fernet
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
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
    import logging
    import twint
    import platform

except:
    print("Downloading missing packages")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    print("Packages installed")
    print("Importing packages")
    from cryptography.fernet import Fernet
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
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
    import logging

    try:
        import twint
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--user", "--upgrade",
                               "git+https://github.com/twintproject/twint.git@origin/master#egg=twint"])
        import twint

if twint.__version__ != "2.1.21":
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--user", "--upgrade",
                           "git+https://github.com/twintproject/twint.git@origin/master#egg=twint"])
    import twint


from _version import version
from CONSTANTS import *
from data_storage import *
from ui import *
from menu import *
from trading import *
from tradoge import *