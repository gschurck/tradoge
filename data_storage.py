from imports import *

file_path = 'data/config.toml'


def get_data():
    return toml.load(file_path)


def save_data(data):
    with open(file_path, "w") as toml_file:
        toml.dump(data, toml_file)


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


def testpackage():
    print("TESTPACKAGE------------------------------------------------------")
