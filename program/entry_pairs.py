from constants import ZSCORE_THRESH, USD_PER_TRADE, USD_MIN_COLLATERAL
from utils import format_number
from public import get_candles_recent
from cointegration import calculate_zscore
from private import is_open_positions
from bot_agent import BotAgent
from pprint import pprint
import pandas as pd
import json


# Open positions
def open_positions(client):

    """
    Manage triggers for finding trade entry
    """

    # Load cointegrated pairs
    df = pd.read_csv("cointegrated_pairs.csv")

    # Get markets for referencing minimum order size, tick size, etc.
    markets = client.public.get_markets().data

    # Initalize container for BotAgent results
    bot_agents = []

    # Find ZScore triggers
    for index, row in df.iterrows():

        # Extract variables
        base_market = row["base_market"]
        quote_market = row["quote_market"]
        hedge_ratio = row["hedge_ratio"]
        half_life = row["half_life"]

        # Get prices
        series_1 = get_candles_recent(client, base_market)
        series_2 = get_candles_recent(client, quote_market)
        
        # Get ZScore
        if len(series_1) > 0 and len(series_1) == len(series_2):
            spread = series_1 - (hedge_ratio * series_2)
            z_score = calculate_zscore(spread).values.tolist()[-1]
        
            # Establish if potential trade
            if abs(z_score) >= ZSCORE_THRESH:

                # Ensure like-for-like not already open (diversify trading)
                is_base_open = is_open_positions(client, base_market)
                is_quote_open = is_open_positions(client, quote_market)

                # Place trade
                if not is_base_open and not is_quote_open:

                    # Determine side
                    base_side = "BUY" if z_score < 0 else "SELL"
                    quote_side = "BUY" if z_score > 0 else "SELL"

                    # Get acceptable price in string format
                    base_price = series_1[-1]
                    quote_price = series_2[-1]
                    accept_base_price = float(base_price) * 1.01 if z_score < 0 else float(base_price) * 0.99
                    accept_quote_price = float(quote_price) * 1.01 if z_score > 0 else float(quote_price) * 0.99
                    failsafe_base_price = float(base_price) * 0.05 if z_score < 0 else float(base_price) * 1.7
                    base_tick_size = markets["markets"][base_market]["tick_size"]
                    quote_tick_size = markets["markets"][quote_market]["tick_size"]

                    # Format prices
                    accept_base_price = format_number(accept_base_price, base_tick_size)
                    
