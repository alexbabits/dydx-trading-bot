### Input the required constants to allow for connection to DYDX, Stark, and Web3 ###

from dydx3 import Client
from web3 import Web3
from messaging import send_telegram_message
import time
from configs import (
  host,
  dydx_api_key,
  dydx_api_secret,
  dydx_api_passphrase,
  stark_private_key,
  eth_address,
  eth_private_key,
  http_provider,
)

# Connect to DYDX
def connect_dydx():

  client = Client(
      host=host(),
      api_key_credentials={
          "key": dydx_api_key(),
          "secret": dydx_api_secret(),
          "passphrase": dydx_api_passphrase(),
      },
      stark_private_key=stark_private_key(),
      eth_private_key=eth_private_key(),
      default_ethereum_address=eth_address(),
      web3=Web3(Web3.HTTPProvider(http_provider()))
  )

  # Confirm client & send message
  account = client.private.get_account()
  quote_balance = account.data["account"]["quoteBalance"]

  print(f"Successfully connected to {host()}!\nAccount Balance: {quote_balance}")
  send_telegram_message(f"Successfully connected to {host()}!\nAccount Balance: {quote_balance}")
  time.sleep(2)

  return client