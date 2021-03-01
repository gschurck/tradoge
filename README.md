[![Github All Releases](https://img.shields.io/github/downloads/gschurck/tradoge/total.svg)]()

Donate :
<a href="https://paypal.me/pools/c/8xeXQlOHn3"><img src="https://logos-marques.com/wp-content/uploads/2020/01/Paypal-logo.png" alt="doge" width="100"/></a>
<a href="https://coinrequest.io/request/cBKHRyzVpKuw5Cq"><img src="https://cryptologos.cc/logos/bitcoin-btc-logo.svg" alt="btc" width="50"/></a>
<a href="https://coinrequest.io/request/tIr7sFblRGQ6PXo"><img src="https://cryptologos.cc/logos/ethereum-eth-logo.svg?v=010" alt="eth" height="50"/></a>
<a href="https://coinrequest.io/request/PDkJ4IyL1JEw2Ab"><img src="https://cryptologos.cc/logos/tether-usdt-logo.svg?v=010" alt="usdt" width="50"/></a>
<a href="https://coinrequest.io/request/bAOicJxeN6y76yF"><img src="https://cryptologos.cc/logos/dogecoin-doge-logo.svg?v=010" alt="doge" width="50"/></a>


# :chart_with_upwards_trend: TraDOGE

Tradoge is a Binance trading bot that instantly buys and sells DOGE cryptocurrency on Binance when Elon Musk tweets about it.

![alt text](https://github.com/gschurck/tradoge/blob/media/tradoge.png?raw=true)

## Main features :

- :thumbsup: User-friendly command-line interface
- :closed_lock_with_key: Binance API keys are encrypted with a password using SHA-256
- :gear: Full configuration can be changed easily in menu, without coding
  - Change tweet refresh frequency, trading pair, sell delay, buying mode and amount to buy
  - :heavy_dollar_sign: Choose between buy a fixed DOGE amount or an adaptative DOGE amount with a fixed dollar amount
- 💱 Binance trading pairs : DOGE/USDT, DOGE/BUSD, DOGE/BTC, DOGE/EUR
- :information_source: Checking for update at start-up

By default, TraDOGE ignores retweets, comments and citations to be safer. Main tweets have more impact.

## Installing

:information_source: I recommend to run tradoge in the [new Windows terminal](https://www.microsoft.com/fr-fr/p/windows-terminal/9n0dx20hk701) for full support of Unicode characters and better visual experience.

### Windows

:inbox_tray: [Download tradoge.zip](https://github.com/gschurck/tradoge/releases)

- Download and unzip
- Run `tradoge.exe`

OR

### Python script

**Require Python 3.7**

**Git :**
```bash
git clone https://github.com/gschurck/tradoge.git
cd tradoge
python -m pip install -r requirements.txt
```
**Then run :**
```bash
cd ..
tradoge.py
```
:warning: If you experience issues during installation try to restart the script a few times.

**If you have errors with twint import, try :**
```bash
pip3 install --upgrade -e git+https://github.com/twintproject/twint.git@origin/master#egg=twint
```
**On Raspberry Py, numpy import can cause an error. Try :**
```bash
sudo apt-get install libatlas-base-dev
```

## Why use Tradoge ?

![alt text](https://github.com/gschurck/tradoge/blob/media/elon1.png?raw=true)
![alt text](https://github.com/gschurck/tradoge/blob/media/graph1.png?raw=true)
**+10%**

------

![alt text](https://github.com/gschurck/tradoge/blob/media/elon2.png?raw=true)
![alt text](https://github.com/gschurck/tradoge/blob/media/graph2.png?raw=true)
**+17.5%**

------

![alt text](https://github.com/gschurck/tradoge/blob/media/elon3.png?raw=true)
![alt text](https://github.com/gschurck/tradoge/blob/media/graph3.png?raw=true)
**+8%**

### Binance issues

If TraDOGE shows "CONNECTED TO YOUR BINANCE ACCOUNT" on login, everything should work on your account.
Just make sure to use a sufficient amount of money when buying, or Binance can return an error.

## Buy me a coffee

If you want to support me, thank you !

My crypto adresses :

DOGE : `DJbbN3nYKMYneJuKU4QKicLjSfggToU4az`

BTC : `bc1q20m4d3f2469q34wpprldhezhw5x4duxxgg7v27`

ETH : `0x65700e91997e3e6320725ba081b028782d94eaca`

USDT : `0x2C95a4aFFCb9A92e38Fcf0943A4ed314EC90bfCB`

BNB : `bnb1q5g5zr8nxqk55lajesk0x4xf8r9yex795az6m4`

XMR : `42VkGVJoQFPAWm5Km1rA1UiEt7hQMdaf9Z3ki1pBA9LR4iaoXDU9S1sMr1ik38HXAsgKvvw8442zKTHPj9dsDxkaGc4amVT`
