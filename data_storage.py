import base64
import os

import toml

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

file_path = 'data/config.toml'


class Config:
    def __init__(self):
        self.config = toml.load('data/config.toml')
        if self.config["binance"]:
            binance = self.config["binance"]
            self.api_key = binance["api_key"]
            self.secret_key = binance["secret_key"]
        # TODO add key verif

    def get_toml(self):
        self.config = toml.load('data/config.toml')
        binance = self.config["binance"]
        self.api_key = binance["api_key"]
        self.secret_key = binance["secret_key"]
        return self.config


def get_data():
    return toml.load(file_path)


def save_data(data):
    print(data)
    with open(file_path, "w", encoding='utf-8') as toml_file:
        toml.dump(data, toml_file)
    print('Saved data to file')


def save_data_to_tradoge(data):
    config_obj = Config()
    config = config_obj.get_toml()

    config['tradoge'].update(data)
    print(data)
    with open(file_path, "w", encoding='utf-8') as toml_file:
        toml.dump(config, toml_file)
    print('Saved data to file')


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

    file_name = 'data/config.toml'
    data = toml.load(file_name)
    data['binance']['api_key'] = api_token
    data['binance']['secret_key'] = secret_token
    data['binance']['salt'] = salt
    save_data(data)


def decrypt_keys(config, password):
    config = config.get_toml()
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