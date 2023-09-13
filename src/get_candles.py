### Returns a df of candlestick data for a market. Used to create the 'tradable_markets' and 'open_positions' dictionaries ###

import pandas as pd
import pandas_ta as ta
import time
from datetime import datetime, timedelta
from configs import API_LIMIT_SIZE, NUM_API_CALLS, resolution_str, time_chunk, entry_ema_value, tp_ema_value, sl_ema_value


def get_candles(client, market):

    to_iso = datetime.utcnow().isoformat() 
    all_candles_df = pd.DataFrame()

    for _ in range(NUM_API_CALLS):

        from_iso = (datetime.fromisoformat(to_iso) - timedelta(minutes=time_chunk())).isoformat()

        candles = client.public.get_candles(
            market=market,
            resolution=resolution_str(),
            from_iso=from_iso,
            to_iso=to_iso,
            limit=API_LIMIT_SIZE
        )
        
        # Convert the chunk of candlestick data into a df
        chunk_of_candles_df = pd.DataFrame(candles.data["candles"])
        chunk_of_candles_df.rename(columns={'startedAt': 'datetime'}, inplace=True)
        chunk_of_candles_df['datetime'] = pd.to_datetime(chunk_of_candles_df['datetime'])
        chunk_of_candles_df.set_index('datetime', inplace=True)
        
        all_candles_df = pd.concat([chunk_of_candles_df, all_candles_df]) # Add the chunk to our total df
        to_iso = from_iso # to_iso becomes the next from_iso 
    
    # Format entire df after all API calls are done
    all_candles_df.sort_index(inplace=True)
    all_candles_df['open'] = pd.to_numeric(all_candles_df['open'], errors='coerce')
    all_candles_df['high'] = pd.to_numeric(all_candles_df['high'], errors='coerce')
    all_candles_df['low'] = pd.to_numeric(all_candles_df['low'], errors='coerce')
    all_candles_df['close'] = pd.to_numeric(all_candles_df['close'], errors='coerce')

    drop_these_columns = ['market', 'resolution', 'updatedAt', 'baseTokenVolume', 'trades', 'usdVolume', 'startingOpenInterest']
    all_candles_df.drop(columns=drop_these_columns, inplace=True)
    
    # Adds TA columns
    all_candles_df['RSI'] = ta.rsi(all_candles_df['close'])
    all_candles_df['ATR'] = ta.atr(all_candles_df['high'], all_candles_df['low'], all_candles_df['close'])
    all_candles_df[f"EMA{entry_ema_value()}"] = ta.ema(all_candles_df['close'], length=entry_ema_value())
    all_candles_df[f"EMA{tp_ema_value()}"] = ta.ema(all_candles_df['close'], length=tp_ema_value())
    all_candles_df[f"EMA{sl_ema_value()}"] = ta.ema(all_candles_df['close'], length=sl_ema_value())
    all_candles_df.fillna(0, inplace=True)

    time.sleep(2)

    return all_candles_df