import subprocess
import sys

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
    import platform
    from pytwitter import Api, StreamApi


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