### Functions required for determining thresholds to enter/exit an order, creation, and execution of an order based on entry and exit strategies ###

import math
import time
from datetime import datetime, timedelta
from messaging import send_telegram_message
from configs import position_size, side, entry_ema_use, entry_rsi_use, entry_ema_value, entry_rsi_value, entry_ema_above, entry_rsi_above, tp_ema_use, tp_ema_value, tp_rsi_use, tp_rsi_value, tp_atr_use, tp_atr_value, pct_gain_use, pct_gain_value, sl_ema_use, sl_ema_value, sl_rsi_use, sl_rsi_value, sl_atr_use, sl_atr_value, pct_loss_use, pct_loss_value


def num_digits_after_decimal(number):
    str_num = str(number)
    if '.' in str_num:
        return len(str_num.split('.')[1])
    else:
        return 0
    
def enter_trade_threshold(latest_candle, market, open_position_names):

    RSI_CHECK = latest_candle["RSI"] > entry_rsi_value() if entry_rsi_above() else latest_candle["RSI"] < entry_rsi_value()
    EMA_CHECK = latest_candle["close"] > latest_candle[f"EMA{entry_ema_value()}"] if entry_ema_above() else latest_candle["close"] < latest_candle[f"EMA{entry_ema_value()}"]

    if entry_rsi_use() and entry_ema_use():
        return RSI_CHECK and EMA_CHECK and (market not in open_position_names)

    if entry_rsi_use() and not entry_ema_use():
        return RSI_CHECK and (market not in open_position_names)

    if entry_ema_use() and not entry_rsi_use():
        return EMA_CHECK and (market not in open_position_names)
    
    return False


def tp_threshold(latest_candle, entryPrice):

    RSI_CHECK = latest_candle["RSI"] > tp_rsi_value()
    EMA_CHECK = latest_candle["close"] > latest_candle[f"EMA{tp_ema_value()}"]
    ATR_CHECK = latest_candle["close"]  > entryPrice + tp_atr_value() * latest_candle["ATR"]
    PCT_CHECK = latest_candle["close"] > entryPrice * pct_gain_value()

    if tp_rsi_use() and tp_ema_use() and not tp_atr_use() and not pct_gain_use():
        return RSI_CHECK and EMA_CHECK

    if tp_rsi_use() and not tp_ema_use() and not tp_atr_use() and not pct_gain_use():
        return RSI_CHECK

    if tp_ema_use() and not tp_rsi_use() and not tp_atr_use() and not pct_gain_use():
        return EMA_CHECK

    if tp_atr_use() and not pct_gain_use():
        return ATR_CHECK
    
    if pct_gain_use() and not tp_atr_use():
        return PCT_CHECK

    return False


def sl_threshold(latest_candle, entryPrice):

    RSI_CHECK = latest_candle["RSI"] < sl_rsi_value()
    EMA_CHECK = latest_candle["close"] < latest_candle[f"EMA{sl_ema_value()}"]
    ATR_CHECK = latest_candle["close"]  < entryPrice - sl_atr_value() * latest_candle["ATR"]
    PCT_CHECK = latest_candle["close"] < entryPrice * pct_loss_value()

    if sl_rsi_use() and sl_ema_use() and not sl_atr_use() and not pct_loss_use():
        return RSI_CHECK and EMA_CHECK

    if sl_rsi_use() and not sl_ema_use() and not sl_atr_use() and not pct_loss_use():
        return RSI_CHECK

    if sl_ema_use() and not sl_rsi_use() and not sl_atr_use() and not pct_loss_use():
        return EMA_CHECK

    if sl_atr_use() and not pct_loss_use():
        return ATR_CHECK
    
    if pct_loss_use() and not sl_atr_use():
        return PCT_CHECK

    return False


def enter_trades(client, tradable_markets_candles_dict, open_positions_list):

    # Initialize counter, get market data, position ID, and expiration time
    num_orders_placed = 0
    markets = client.public.get_markets()
    account_response = client.private.get_account()
    server_time = client.public.get_time()
    position_id = account_response.data["account"]["positionId"]
    expiration = datetime.fromisoformat(server_time.data["iso"].replace("Z", "")) + timedelta(seconds=70)

    # grab all open position market names 
    open_position_names = []
    for position in open_positions_list:
        open_position_names.append(position['market'])

    # Loop through each market and create entry orders if applicable
    for market, df in tradable_markets_candles_dict.items():

        latest_candle = df.iloc[-1]

        if enter_trade_threshold(latest_candle, market, open_position_names):

            # Grab info about market
            close_price = float(latest_candle['close'])
            tickSize = markets.data["markets"][market]['tickSize']
            stepSize = float(markets.data["markets"][market]['stepSize'])
            
            # formatting for size and price parameters
            size_raw = position_size() / close_price
            size_adj = math.floor(size_raw / stepSize) * stepSize
            size = str(round(size_adj, num_digits_after_decimal(stepSize)))

            if side() == "BUY":
                worst_execution_price = str(round(2 * close_price, num_digits_after_decimal(tickSize)))
            else:
                worst_execution_price = str(round(0.5 * close_price, num_digits_after_decimal(tickSize)))

            place_order = client.private.create_order(
                position_id=position_id,
                market=market,
                side=side(),
                order_type="MARKET",
                post_only=False,
                size=size,
                price=worst_execution_price,
                limit_fee='0.015',
                expiration_epoch_seconds=expiration.timestamp(),
                time_in_force="FOK",
                reduce_only=False 
            )

            num_orders_placed += 1
            send_telegram_message(f"Placed {side()} order for {size} {market}. (${position_size()})")
            print(f"Placed {side()} order for {size} {market}. (${position_size()})")
            time.sleep(2)

    if num_orders_placed == 0:
        send_telegram_message("No trades found while looking for potential entries.")
    else:
        send_telegram_message(f"{num_orders_placed} trade(s) found and placed while looking for potential entries.")


def exit_trades(client, open_positions_candles_dict, open_positions_list):

    # Initialize counter, Get market data, position ID, and expiration time
    num_orders_placed = 0
    markets = client.public.get_markets()
    account_response = client.private.get_account()
    server_time = client.public.get_time()
    position_id = account_response.data["account"]["positionId"] 
    expiration = datetime.fromisoformat(server_time.data["iso"].replace("Z", "")) + timedelta(seconds=70)

    # Loop through open positions candles and create exit orders if applicable
    for market, df in open_positions_candles_dict.items():
        # Loop through open positions data and find the size/entry/side data needed
        for position in open_positions_list:
            if position['market'] == market:
                entryPrice = float(position['entryPrice'])
                size = str(abs(float(position['size'])))
                if position['side'] == "LONG":
                    side = "SELL"
                else:
                    side = "BUY"
                break

        latest_candle = df.iloc[-1]

        if tp_threshold(latest_candle, entryPrice) or sl_threshold(latest_candle, entryPrice):

            # Grab info about market
            close_price = float(latest_candle['close'])
            tickSize = markets.data["markets"][market]['tickSize']

            if side == "SELL":
                worst_execution_price = str(round(0.5 * close_price, num_digits_after_decimal(tickSize)))
            else:
                worst_execution_price = str(round(2 * close_price, num_digits_after_decimal(tickSize)))

            place_order = client.private.create_order(
                position_id=position_id,
                market=market,
                side=side,
                order_type="MARKET",
                post_only=False,
                size=size,
                price=worst_execution_price,
                limit_fee='0.015',
                expiration_epoch_seconds=expiration.timestamp(),
                time_in_force="FOK",
                reduce_only=True
            )

            num_orders_placed += 1
            send_telegram_message(f"Placed {side} order for {size} {market}.")
            print(f"Placed {side} order for {size} {market}.")
            time.sleep(2)

    if num_orders_placed == 0:
        send_telegram_message("No trades found while looking for potential exits.")
    else:
        send_telegram_message(f"{num_orders_placed} trade(s) found and placed while looking for potential exits.")