### Function for telegram messaging ###

import requests
from configs import telegram_token, telegram_chat_id

def send_telegram_message(message):
  url = f"https://api.telegram.org/bot{telegram_token()}/sendMessage?chat_id={telegram_chat_id()}&text={message}"
  res = requests.get(url)
  if res.status_code == 200:
    return "sent"
  else:
    return "failed"