### Contains useful config settings ###

from dydx3.constants import API_HOST_GOERLI, API_HOST_MAINNET
from decouple import config
import json

# ---------------- .env variables ----------------

# Telegram 
TELEGRAM_TOKEN = config("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = config("TELEGRAM_CHAT_ID")

# Ethereum Address & Private Key
ETHEREUM_ADDRESS = config("ETHEREUM_ADDRESS")
ETH_PRIVATE_KEY = config("ETH_PRIVATE_KEY")

# MAINNET KEYS & HTTP PROVIDER URL (Must be on Mainnet on DYDX)
STARK_PRIVATE_KEY_MAINNET = config("STARK_PRIVATE_KEY_MAINNET")
DYDX_API_KEY_MAINNET = config("DYDX_API_KEY_MAINNET")
DYDX_API_SECRET_MAINNET = config("DYDX_API_SECRET_MAINNET")
DYDX_API_PASSPHRASE_MAINNET = config("DYDX_API_PASSPHRASE_MAINNET")
HTTP_PROVIDER_MAINNET = config("HTTP_PROVIDER_MAINNET")

# TESTNET KEYS (Must be on Testnet on DYDX)
STARK_PRIVATE_KEY_TESTNET = config("STARK_PRIVATE_KEY_TESTNET")
DYDX_API_KEY_TESTNET = config("DYDX_API_KEY_TESTNET")
DYDX_API_SECRET_TESTNET = config("DYDX_API_SECRET_TESTNET")
DYDX_API_PASSPHRASE_TESTNET = config("DYDX_API_PASSPHRASE_TESTNET")
HTTP_PROVIDER_TESTNET = config("HTTP_PROVIDER_TESTNET")



# ---------------- static constants ----------------
TOTAL_CANDLES = 400
RESOLUTION_DICT = {"5MINS": 5, "15MINS": 15, "30MINS": 30, "1HOUR": 60, "4HOURS": 240, "1DAY": 1440}
API_LIMIT_SIZE = min(100, TOTAL_CANDLES ) # 100, unless TOTAL_CANDLES < 100
NUM_API_CALLS = TOTAL_CANDLES  // API_LIMIT_SIZE

# ---------------- dynamic user input configs ----------------

# Entry

def side():
    with open('configs.json', 'r') as f:
        config_data = json.load(f)
    return config_data['SIDE']

def entry_ema_use():
    with open('configs.json', 'r') as f:
        config_data = json.load(f)
    return config_data['ENTRY_EMA_USE']

def entry_rsi_use():
    with open('configs.json', 'r') as f:
        config_data = json.load(f)
    return config_data['ENTRY_RSI_USE']

def entry_ema_value():
    with open('configs.json', 'r') as f:
        config_data = json.load(f)
    return config_data['ENTRY_EMA_VALUE']

def entry_rsi_value():
    with open('configs.json', 'r') as f:
        config_data = json.load(f)
    return config_data['ENTRY_RSI_VALUE']

def entry_ema_above():
    with open('configs.json', 'r') as f:
        config_data = json.load(f)
    return config_data['ENTRY_EMA_ABOVE']

def entry_rsi_above():
    with open('configs.json', 'r') as f:
        config_data = json.load(f)
    return config_data['ENTRY_RSI_ABOVE']

def position_size():
    with open('configs.json', 'r') as f:
        config_data = json.load(f)
    return config_data['POSITION_SIZE_USD']

def resolution_str():
    with open('configs.json', 'r') as f:
        config_data = json.load(f)
    return config_data['RESOLUTION_STR']

def resolution_int():
    return RESOLUTION_DICT[resolution_str()]

def time_chunk():
    return API_LIMIT_SIZE * resolution_int()


# TP
def tp_ema_use():
    with open('configs.json', 'r') as f:
        config_data = json.load(f)
    return config_data['TP_EMA_USE']

def tp_ema_value():
    with open('configs.json', 'r') as f:
        config_data = json.load(f)
    return config_data['TP_EMA_VALUE']

def tp_rsi_use():
    with open('configs.json', 'r') as f:
        config_data = json.load(f)
    return config_data['TP_RSI_USE']

def tp_rsi_value():
    with open('configs.json', 'r') as f:
        config_data = json.load(f)
    return config_data['TP_RSI_VALUE']

def tp_atr_use():
    with open('configs.json', 'r') as f:
        config_data = json.load(f)
    return config_data['TP_ATR_USE']

def tp_atr_value():
    with open('configs.json', 'r') as f:
        config_data = json.load(f)
    return config_data['TP_ATR_VALUE']

def pct_gain_use():
    with open('configs.json', 'r') as f:
        config_data = json.load(f)
    return config_data['PCT_GAIN_USE']

def pct_gain_value():
    with open('configs.json', 'r') as f:
        config_data = json.load(f)
    return config_data['PCT_GAIN_VALUE']

# SL
def sl_ema_use():
    with open('configs.json', 'r') as f:
        config_data = json.load(f)
    return config_data['SL_EMA_USE']

def sl_ema_value():
    with open('configs.json', 'r') as f:
        config_data = json.load(f)
    return config_data['SL_EMA_VALUE']

def sl_rsi_use():
    with open('configs.json', 'r') as f:
        config_data = json.load(f)
    return config_data['SL_RSI_USE']

def sl_rsi_value():
    with open('configs.json', 'r') as f:
        config_data = json.load(f)
    return config_data['SL_RSI_VALUE']

def sl_atr_use():
    with open('configs.json', 'r') as f:
        config_data = json.load(f)
    return config_data['SL_ATR_USE']

def sl_atr_value():
    with open('configs.json', 'r') as f:
        config_data = json.load(f)
    return config_data['SL_ATR_VALUE']

def pct_loss_use():
    with open('configs.json', 'r') as f:
        config_data = json.load(f)
    return config_data['PCT_LOSS_USE']

def pct_loss_value():
    with open('configs.json', 'r') as f:
        config_data = json.load(f)
    return config_data['PCT_LOSS_VALUE']


# Control Panel
def mode():
    with open('configs.json', 'r') as f:
        config_data = json.load(f)
    return config_data['MODE']

def enter_trades_bool():
    with open('configs.json', 'r') as f:
        config_data = json.load(f)
    return config_data['ENTER_TRADES']

def exit_trades_bool():
    with open('configs.json', 'r') as f:
        config_data = json.load(f)
    return config_data['EXIT_TRADES']


# Getting and setting personal info as Testnet/Mainnet depending on MODE selected
def eth_address():
    return ETHEREUM_ADDRESS

def eth_private_key():
    return ETH_PRIVATE_KEY

def telegram_token():
    return TELEGRAM_TOKEN

def telegram_chat_id():
    return TELEGRAM_CHAT_ID

def host():
    return API_HOST_MAINNET if mode() == "PRODUCTION" else API_HOST_GOERLI

def stark_private_key():
    return STARK_PRIVATE_KEY_MAINNET if mode() == "PRODUCTION" else STARK_PRIVATE_KEY_TESTNET

def dydx_api_key():
    return DYDX_API_KEY_MAINNET if mode() == "PRODUCTION" else DYDX_API_KEY_TESTNET

def dydx_api_secret():
    return DYDX_API_SECRET_MAINNET if mode() == "PRODUCTION" else DYDX_API_SECRET_TESTNET

def dydx_api_passphrase():
    return DYDX_API_PASSPHRASE_MAINNET if mode() == "PRODUCTION" else DYDX_API_PASSPHRASE_TESTNET

def http_provider():
    return HTTP_PROVIDER_MAINNET if mode() == "PRODUCTION" else HTTP_PROVIDER_TESTNET