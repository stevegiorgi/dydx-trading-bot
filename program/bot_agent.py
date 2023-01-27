from private import check_order_status, place_market_order
from datetime import datetime, timedelta
from pprint import pprint
import time


class BotAgent:

    """
    Primary function of BotAgent
    """

    # Initalize class
    def __init__(
        self,
        client,
        market_1,
        market_2,
        base_side,
        base_size,
        base_price,
        quote_side,
        quote_size,
        quote_price,
        accept_failsafe_base_price,
        z_score,
        half_life,
        hedge_ratio
    ):

        # Initalize class variables
        self.client = client
        self.market_1 = market_1
        self.market_2 = market_2
        self.base_side = base_side
        self.base_size = base_size
        self.base_price = base_price
        self.quote_side = quote_side
        self.quote_size = quote_size
        self.quote_price = quote_price
        self.accept_failsafe_base_price = accept_failsafe_base_price
        self.z_score = z_score
        self.half_life = half_life
        self.hedge_ratio = hedge_ratio

        # Initalize output variable

        # Pair status options (FAILED, LIVE, CLOSE, ERROR)
        self.order_dict = {
            "market_1": market_1,
            "market_2": market_2,
            "hedge_ratio": hedge_ratio,
            "z_score": z_score,
            "order_id_m1": "",
            "order_m1_size": base_size,
            "order_m1_side": base_side,
            "order_time_m1": "",            
            "order_id_m2": "",
            "order_m2_size": quote_size,
            "order_m2_side": quote_side,
            "order_time_m2": "",
            "pair_status": "",
            "comments": "",
        }

    # Check order status by ID        
    def check_order_status_by_id(self, order_id):

        time.sleep(2)

        # Check order status
        order_status = check_order_status(self.client, order_id)

        # Check: if order cancelled move onto next pair
        if order_status == "CANCELED":
            print(f"{self.market_1} vs {self.market_2}: Order cancelled")
            self.order_dict["pair_status"] = "FAILED"
            return "failed"

        # Check: if order not filled wait until expiration
        if order_status != "FAILED":
            time.sleep(15)
            order_status = check_order_status(self.client, order_id)

            # Check: if order cancelled move onto next pair
            if order_status == "CANCELED":
                print(f"{self.market_1} vs {self.market_2}: Order cancelled")
                self.order_dict["pair_status"] = "FAILED"
                return "failed"

            # Check: if not filled, cancel order
            if order_status != "FILLED":
                self.client.private.cancel_order(order_id=order_id)
                self.order_dict["pair_status"] = "ERROR"
                print(f"{self.market_1} vs {self.market_2}: Order error")
                return "error"

        return "live"

    # Open trades
    def open_trades(self):

        # Print status: opening first order
        print("----")
        print(f"{self.market_1}: Placing first order...")
        print(f"side: {self.base_side}, size: {self.base_size}, price: {self.base_price}")        
        print("----")

        # Place base order
        try:
            base_order = place_market_order(
                self.client,
                market=self.market_1,
                side=self.base_side,
                size=self.base_size,
                price=self.base_price,
                reduce_only=False                
            )

            # Store order ID
            self.order_dict["order_id_m1"] = base_order["order"]["id"]
            self.order_dict["order_time_m1"] = datetime.now().isoformat()
            
        except Exception as e:
            self.order_dict["pair_status"] = "ERROR"
            self.order_dict["comments"] = f"Market 1: {self.market_1}: {e}"

            return self.order_dict

        # Ensure order is live prior to processing
        order_status_m1 = self.check_order_status_by_id(self.order_dict["order_id_m1"])

        # Check: abort if order fails
        if order_status_m1 != "live":
            self.order_dict["pair_status"] = "ERROR"
            self.order_dict["comments"] = f"Failed to fill: {self.market_1}"
            return self.order_dict

        # Print status: opening second order
        print("----")
        print(f"{self.market_2}: Placing second order...")
        print(f"side: {self.quote_side}, size: {self.quote_size}, price: {self.quote_price}")
        print("----")

        # Place base order
        try:
            quote_order = place_market_order(
                self.client,
                market=self.market_2,
                side=self.quote_side,
                size=self.quote_size,
                price=self.quote_price,
                reduce_only=False
            )

            # Store order ID
            self.order_dict["order_id_m2"] = quote_order["order"]["id"]
            self.order_dict["order_time_m2"] = datetime.now().isoformat()
            
        except Exception as e:
            self.order_dict["pair_status"] = "ERROR"
            self.order_dict["comments"] = f"Market 2: {self.market_2}: {e}"

            return self.order_dict  

        # Ensure order is live prior to processing
        order_status_m2 = self.check_order_status_by_id(self.order_dict["order_id_m2"])

        # Check: abort if order failed
        if order_status_m2 != "live":
            self.order_dict["pair_status"] = "ERROR"
            self.order_dict["comments"] = f"Failed to fill: {self.market_2}"

            # Close order 1
            try:
                close_order = place_market_order(
                    self.client,
                    market=self.market_1,
                    side=self.quote_side,
                    size=self.base_size,
                    price=self.accept_failsafe_base_price,
                    reduce_only=True
                )

                # Ensure order is live before proceeding
                time.sleep(2)
                order_status_close_order = check_order_status(self.client, close_order["order"]["id"])
                if order_status_close_order != "FILLED":
                    print("ABORT PROGRAM")
                    print("Unexpected error")
                    print(order_status_close_order)
                    exit(1)

            except Exception as e:
                self.order_dict["pair_status"] = "ERROR"
                self.order_dict["comments"] = f"Close market 1: {self.market_1}: {e}"
                print("ABORT PROGRAM")
                print("Unexpected error")
                print(order_status_close_order)
                exit(1)
        
        # Return success result
        else:
            self.order_dict["pair_status"] = "LIVE"
            return self.order_dict
            