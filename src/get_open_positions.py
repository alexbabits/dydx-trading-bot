### Makes a list of dictionaries of open positions and associated information about them ###

from messaging import send_telegram_message
import time

def get_open_positions(client, tradable_markets):

    time.sleep(2)

    open_positions_dict = {}
    open_positions_list = []
    position_names = []

    # Look for open positions from all tradable markets
    for market in tradable_markets:
        open_positions_dict[market] = client.private.get_positions(
            market=market,
            status='OPEN'
        )

    # Organize open position data into a list of dictionaries
    for market_data in open_positions_dict.values():
        for position in market_data.data['positions']:
            open_positions_list.append({
                'market': position['market'], 
                'entryTime': position['createdAt'],
                'entryPrice': position['entryPrice'], 
                'side': position['side'], 
                'size': position['size']})
            
    for position in open_positions_list:
        position_names.append(position['market'])
    send_telegram_message(f"Found {len(open_positions_list)} open position(s).\n{position_names}")
    time.sleep(2)

    return open_positions_list

# Note: print(open_positions_dict[market].data['positions']) will print the data info for every tradable market inside the 1st for loop.