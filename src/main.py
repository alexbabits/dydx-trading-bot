from configs import enter_trades_bool, exit_trades_bool, resolution_int
from connect import connect_dydx
from get_tradable_markets import get_tradable_markets
from get_open_positions import get_open_positions
from execute_trades import enter_trades, exit_trades
from make_dicts import make_tradable_candles_dict, make_open_positions_candles_dict
from messaging import send_telegram_message
import schedule
import time
from queue import Queue

stop_queue = Queue()
stop_message_sent = False # Flag to not double send telegram message if stopped in middle of look_for_trades

def check_stop_queue():
    global stop_message_sent
    if not stop_queue.empty():
        if not stop_message_sent:
            send_telegram_message("Stopped Bot.")
            stop_message_sent = True
        return True

def look_for_trades():

  ### Connect, get tradable markets & any open positions ###
  if check_stop_queue(): return 
  client = connect_dydx()
  if check_stop_queue(): return 
  tradable_markets = get_tradable_markets(client)
  if check_stop_queue(): return 
  open_positions_list = get_open_positions(client, tradable_markets)
  
  ### Looks for Trade Exits  ###
  if check_stop_queue(): return 
  if exit_trades_bool() and open_positions_list:
    open_positions_candles_dict = make_open_positions_candles_dict(client, open_positions_list)
    if check_stop_queue(): return 
    exit_trades(client, open_positions_candles_dict, open_positions_list)
  
  ### Looks for Trade Entries ###
  if check_stop_queue(): return 
  if enter_trades_bool():
    tradable_markets_candles_dict = make_tradable_candles_dict(client, tradable_markets)
    if check_stop_queue(): return 
    enter_trades(client, tradable_markets_candles_dict, open_positions_list)

def start_bot():
    global stop_message_sent
    stop_queue.queue.clear()
    stop_message_sent = False
    look_for_trades()
    if not stop_message_sent:
      send_telegram_message(f"Hibernating... will look for trades again in {resolution_int()} minutes.")
    schedule.every(resolution_int()).minutes.do(look_for_trades)
    while True:
        if check_stop_queue(): return 
        schedule.run_pending()
        time.sleep(1)

def stop_bot():
    stop_queue.put("STOP")

if __name__ == "__main__":
    start_bot()


"""    
Note: After making the dictionaries for open positions or tradable market, optional check of data afterwards:

    for market, df in open_positions_candles_dict.items():
      print(f"Market: {market}\n{df.tail(2)}\n")

    for market, df in open_positions_candles_dict.items():
      print(f"Market: {market}\n{df.tail(2)}\n")

"""