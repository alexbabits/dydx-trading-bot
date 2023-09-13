### Fetches all Tradable Markets ###

from messaging import send_telegram_message
import time

def get_tradable_markets(client):

    markets = client.public.get_markets()
    tradable_markets = []
    
    # Find all tradable pairs
    for key in markets.data["markets"].keys():
        if markets.data["markets"][key]["status"] == "ONLINE":
            tradable_markets.append(key)
    
    send_telegram_message(f"Found {len(tradable_markets)} tradable markets for DYDX!")
    time.sleep(2)

    return tradable_markets


# Note: markets.data["markets"] accesses all the markets data. The keys are the markets like 'BTC-USD'.
# Note: indexPrice inside of markets.data["markets"].values() gets current price