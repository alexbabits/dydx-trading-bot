## Features

Autonomous DYDX v3 trading bot with telegram alerts. Alternates between looking for entries/exits and hibernation at the desired time frame. 

![](/pictures/ui.png)

- Pick your position size (USD), time frame (candlestick & hibernation time), and side of the trade (Long/Short).
- Choose simple entry strategies based on an EMA and/or RSI.
- take profit/stop loss exit strategies based on EMA and/or RSI, or based on ATR factor from entry, or raw percent loss/gain.
- Control panel to Stop/Start bot. Allows for switching between testnet and mainnet, dark/light mode, and the choice for entering and/or exiting trades.
- Stop the bot at any time (besides creation of dictionaries right before looking for entries/exits) thanks to queues. Uses scheduler to hibernate.


One full test loop with settings that always buy/sell some coins:

![](/pictures/telegrampicture.png)


## Structure Overview

- Install requirements (auto-py-to-exe is optional).
- Run via terminal with `python main_window.py` once in the `src` directory. 
- Or create an .exe with auto-py-to-exe (`auto-py-to-exe main_window.py` and then under additional files, add everything from `src`, including `theme`, but not `main_window.py`. Also add the external packages from requirements as folders like `tksvg`, `dydx`, `web3`, and just incase `schedule`, `pandas-ta`, and `pandas`)

1. connect --> grab available markets -->
2. Look at open positions --> Look for exits -->
3. Look at open positions --> Look for entries -->
4. Disconnect and hibernate --> 1.

- `main.py` Contains the above logic, infinitely loops unless bot is stopped. Before every time it looks for trades, it must update the current candlestick and TA data for the markets.
- `main_window.py` Contains the frontend tkinter GUI code with functions for widgets to send personal user input data to `.env` or general user input to `configs.json`.
- `configs.py` Contains exported `.env` variables and uses functions to load and return user input configs from `configs.json`. Whenever a config is needed, the appropriate `configs.py` function is called from within other modules to grab the latest user input from `configs.json`.
- `connect.py` Forms the connection with dydx (the exchange), stark (the L2 solution to place orders), and your wallet info to sign orders.
- `execute_trades.py` Handles entry and exix strategies via simple thresholds and the logic for placing entry and exit trades.
- `get_candles.py` Creates the dataframe of candlestick and TA information to append to a dictionary of markets in `make_dicts.py`.
- `get_open_positions.py` Returns a list of each open trade and it's associated information.
- `get_tradable_markets.py` Returns a list of the names for all currently active markets on DYDX.
- `make_dicts.py` Contains two similar functions to append the candlestick dataframes from `get_candles.py` to all tradable markets or open position markets depending on what is needed.
- `messaging.py` Function to send telegram messages.
- `sun-valley.tcl` Tkinter Windows 11 themed.
- `theme` Directory houses light and dark .svg images and .tcl for the theme.


## Where to Get .env Variables

- Gunbot tutorial for getting `dydx` and `stark` info: https://docs.gunthy.org/guides/various/defiexchange/dydx-api-key/. tl;dr, if your metamask wallet is connected to dydx you can go to dev tools (F12) --> application --> local storage --> trade.stage.dydx and then grab the dydx and stark info.
- My whale watcher bot describes how to get `telegram token` and `telegram chat id`: https://github.com/alexbabits/whale-watcher


## Useful Links

- Inspired from Udemy Course: https://www.udemy.com/course/dydx-pairs-trading-bot-build-in-python-running-in-the-cloud
- DYDX API Documentation: https://dydxprotocol.github.io/v3-teacher/#terms-of-service-and-privacy-policy
- Alchemy: https://dashboard.alchemy.com/apps
- DYDX Python Examples: https://github.com/dydxprotocol/dydx-v3-python/blob/master/examples/orders.py
- pandas_ta: https://github.com/twopirllc/pandas-ta
- sunvalley theme: https://github.com/rdbende/Sun-Valley-ttk-theme-svg
- png to ico: https://video-cutter-js.com/png2icojs/
- If "ImportError: cannot import name 'getargspec' from 'inspect'": https://github.com/ethereum/web3.py/issues/2704 (go into 'parsimonious' in site-packages for your venv, inside expressions.py, change the two instances of getargspec to getfullargspec)


## TO DO/Nice Things to Have

- Mute option for telegram notificatoins (Or less verbose communication for shorter time frame search settings like 5MINS/15MINS).
- Trailing stop losses.
- Multiple take profit levels.
- More indicators.
- Choice of ohlc/4, hlc/3, or close for indicator calculation.
- More robust error handling.
- More robust testing.
- Disable all widgets except stop button when start is pressed.
- Numeric only entries for spinboxes.