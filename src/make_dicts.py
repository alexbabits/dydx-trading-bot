### Makes a dictionaries with the keys as the markets and the values as the associated candlestick dataframe information ###

from get_candles import get_candles
from messaging import send_telegram_message
import time

def make_tradable_candles_dict(client, tradable_markets):

    send_telegram_message("Getting up to date candle and TA data for each tradable market...\nIt takes about 5 seconds per market.")

    tradable_markets_candles_dict = {}

    for market in tradable_markets:
        tradable_markets_candles_dict[market] = get_candles(client, market)

    send_telegram_message("Successfully made up to date dictionary for each tradable market!")
    time.sleep(2)

    return tradable_markets_candles_dict


def make_open_positions_candles_dict(client, open_positions_list):

    send_telegram_message("Getting up to date candle and TA data for each open position...\nIt takes about 5 seconds per market.")

    open_positions_candles_dict = {}

    for position_info in open_positions_list:
        market_name = position_info['market']
        open_positions_candles_dict[market_name] = get_candles(client, market_name)

    send_telegram_message("Successfully made up to date dictionary for each open position!")
    time.sleep(2)

    return open_positions_candles_dict