[![Github All Releases](https://img.shields.io/github/downloads/gschurck/tradoge/total.svg)]()
<!--
Donate :
<a href="https://paypal.me/pools/c/8xeXQlOHn3"><img src="https://logos-marques.com/wp-content/uploads/2020/01/Paypal-logo.png" alt="doge" width="100"/></a>
<a href="https://coinrequest.io/request/cBKHRyzVpKuw5Cq"><img src="https://cryptologos.cc/logos/bitcoin-btc-logo.svg" alt="btc" width="50"/></a>
<a href="https://coinrequest.io/request/tIr7sFblRGQ6PXo"><img src="https://cryptologos.cc/logos/ethereum-eth-logo.svg?v=010" alt="eth" height="50"/></a>
<a href="https://coinrequest.io/request/PDkJ4IyL1JEw2Ab"><img src="https://cryptologos.cc/logos/tether-usdt-logo.svg?v=010" alt="usdt" width="50"/></a>
<a href="https://coinrequest.io/request/bAOicJxeN6y76yF"><img src="https://cryptologos.cc/logos/dogecoin-doge-logo.svg?v=010" alt="doge" width="50"/></a>


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
-->

# :chart_with_upwards_trend: TraDOGE

Tradoge is a Binance trading bot that instantly buys and sells DOGE cryptocurrency on Binance when Elon Musk tweets about it.

## How it works

1. The bot listens to Elon Musk's tweets
2. When Elon Musk tweets about DOGE, the bot buys DOGE on Binance with leverage
3. The bot sells DOGE after a certain delay

## Requirements

- [Docker](https://docs.docker.com/get-docker/) installed on your machine
- [Binance account](https://www.binance.com/activity/referral-entry/CPA?ref=CPA_00IME7D2OT) (with API keys)
- A Binance Isolated Margin account with an available balance (**the total amount of the isolated margin account 
  will be used to buy DOGE**)
## Installation

### 1. Download files

#### With `git`

Run the following command in your terminal :

```bash
git clone https://github.com/gschurck/tradoge.git && \
cd tradoge && \
cp config/config.example.yaml config/config.yaml
```

#### Without `git`

Run the following command in your terminal :

```bash
mkdir tradoge && \
cd tradoge && \
curl -O https://raw.githubusercontent.com/gschurck/tradoge/refs/heads/main/docker-compose.yml && \
mkdir -p config data && \
curl -o config/config.example.yaml https://raw.githubusercontent.com/gschurck/tradoge/refs/heads/main/config/config.example.yaml && \
cp config/config.example.yaml config/config.yaml
```

### 2. Configuration

Fill the config values in file `config/config.yaml` :
- Twitter (X) credentials
- Binance API keys with access to Margin trading
- The Quote Currency you want to buy DOGE with (USDT, USDC, BTC...)

Transfer to your isolated margin account the amount of the quote currency you want to use to buy DOGE.
Set the leverage you want for this isolated margin account in the Binance interface (x1, x2, x3, x5...). The bot will 
use the last leverage you set.

=> If you want to trade on USDC/DOGE and have 100 USDC in your isolated margin account with 5x leverage, the bot will 
buy 500 
USDC worth of DOGE.

### 3. Start TraDOGE

Run the following command in your terminal in your `tradoge` directory :

```bash
docker compose up
```

After building the Docker image, the bot will start and should display the following message :

```
pc:tradoge:% docker compose logs
tradoge-1  | 2025/02/25 23:32:02 Config file loaded successfully
tradoge-1  | 2025/02/25 23:32:02 Trading pairs:
tradoge-1  | 2025/02/25 23:32:02 1. DOGE/USDC
tradoge-1  | 2025/02/25 23:32:02    Twitter search keywords: doge, dogecoin
tradoge-1  | 2025/02/25 23:32:02 Logged in to Twitter
tradoge-1  | 2025/02/25 23:32:02 Query: (doge OR dogecoin) (from:elonmusk) -filter:replies
tradoge-1  | 2025/02/25 23:32:02 Start to search for new tweets every 20 seconds...
```

If you see an error message, check your configuration in the `config/config.yaml` file.
Now you can stop the bot with `Ctrl+C` and start it in detached mode to let it run in the background :

```bash
docker compose up -d
```

### 4. Stop TraDOGE

To stop the bot, run the following command in your terminal in your `tradoge` directory :

```bash
docker compose down
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

ETH : `0x2C95a4aFFCb9A92e38Fcf0943A4ed314EC90bfCB`

USDT : `0x2C95a4aFFCb9A92e38Fcf0943A4ed314EC90bfCB`

BNB : `bnb1q5g5zr8nxqk55lajesk0x4xf8r9yex795az6m4`

XMR : `42VkGVJoQFPAWm5Km1rA1UiEt7hQMdaf9Z3ki1pBA9LR4iaoXDU9S1sMr1ik38HXAsgKvvw8442zKTHPj9dsDxkaGc4amVT`
