from constants import ABORT_ALL_POSITIONS, FIND_COINTEGRATED, PLACE_TRADES
from connections import connect_dydx
from private import abort_all_positions
from public import construct_market_prices
from cointegration import store_cointegration_results
from entry_pairs import open_positions


if __name__ == "__main__":                                                                  

    # Connect to client
    try:
        print("Connecting to client...")
        client = connect_dydx()
    except Exception as e:
        print("Error connecting to client: ", e)
        exit(1)


# Abort all open positions
if ABORT_ALL_POSITIONS:
    try:
        print("Closing all positions...")
        close_orders = abort_all_positions(client)
    except Exception as e:
        print("Error closing positions: ", e)
        exit(1)


# Find cointegrated pairs
if FIND_COINTEGRATED:

    # Construct market prices
    try:
        print("Fetching market prices...")
        df_market_prices = construct_market_prices(client)
    except Exception as e:
        print("Error constructing market prices: ", e)
        exit(1)

    # Store cointegrated pairs
    try:
        print("Storing cointegrated pairs...")
        stores_result = store_cointegration_results(df_market_prices)
        if stores_result != "saved":
            print("Error saving cointegrated pairs")
            exit(1)
    except Exception as e:
        print("Error saving cointegrated pairs: ", e)
        exit(1)




# Place trades
if PLACE_TRADES:
    try:
        print("Finding trade opportunities...")
        open_positions(client)
    except Exception as e:
        print("Error trading pairs: ", e)
        exit(1)