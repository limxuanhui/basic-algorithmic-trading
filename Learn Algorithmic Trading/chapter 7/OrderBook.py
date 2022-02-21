class OrderBook:
    def __init__(self, gw_2_ob=None, ob_2_ts=None):
        self.list_asks = []
        self.list_bids = []
        self.gw_2_ob = gw_2_ob
        self.ob_2_ts = ob_2_ts
        self.current_bid = None
        self.current_ask = None

    def handle_order_from_gateway(self, order=None):
        if self.gw_2_ob is None:
            print("Simulation mode")
            self.handle_order(order)
        elif len(self.gw_2_ob) > 0:
            order_from_gw = self.gw_2_ob.popleft()
            self.handle_order(order_from_gw)

    def handle_order(self, order):
        if order["action"] == "new":
            self.handle_new(order)
        elif order["action"] == "modify":
            self.handle_modify(order)
        elif order["action"] == "delete":
            self.handle_delete(order)
        else:
            print("Error-Cannot handle this action")
        return self.check_generate_top_of_book_event()

    def handle_new(self, order):
        if order["side"] == "bid":
            self.list_bids.append(order)
            self.list_bids.sort(key=lambda x: x["price"], reverse=True)

        elif order["side"] == "ask":
            self.list_asks.append(order)
            self.list_asks.sort(key=lambda x: x["price"])

    def handle_modify(self, order):
        """
        Searches order in list of orders, if order exists, modify its quantity provided that we are reducing it.
        :param order:
        :return:
        """
        ord = self.find_order_in_a_list(order)
        if ord["quantity"] > order["quantity"]:
            ord["quantity"] = order["quantity"]
        else:
            print("Incorrect size")
        return None

    def handle_delete(self, order):
        """
        Removes order from list of orders by checking with order id.
        :param order:
        :return:
        """
        lookup_list = self.get_list(order)
        ord = self.find_order_in_a_list(order, lookup_list)
        if ord is not None:
            lookup_list.remove(ord)
        return None

    def get_list(self, order):
        if "side" in order:
            if order["side"] == "bid":
                lookup_list = self.list_bids
            elif order["side"] == "ask":
                lookup_list = self.list_asks
            else:
                print("Incorrect side")
                return None
            return lookup_list
        else:
            for ord in self.list_bids:
                if ord["id"] == order["id"]:
                    return self.list_bids
            for ord in self.list_asks:
                if ord["id"] == order["id"]:
                    return self.list_asks
            return None

    def find_order_in_a_list(self, order, lookup_list=None):
        if lookup_list is None:
            lookup_list = self.get_list(order)
        if lookup_list is not None:
            for ord in lookup_list:
                if ord["id"] == order['id']:
                    return ord
            print(f"Order not found id = {order['id']}")
        return None

    def create_book_event(self, bid, offer):
        """
        Creates a dictionary representing a book event
        :param bid:
        :param offer:
        :return:
        """
        book_event = {
            "bid_price": bid["price"] if bid else -1,
            "bid_quantity": bid["quantity"] if bid else -1,
            "offer_price": offer["price"] if offer else -1,
            "offer_quantity": offer["quantity"] if offer else -1,
        }
        return book_event

    def check_generate_top_of_book_event(self):
        """
        Creates a book_event when the top of the book has changed.
        :return:
        """
        tob_changed = False
        if not self.list_bids:
            if self.current_bid is not None:
                tob_changed = True
            if not self.current_bid:
                if self.current_bid != self.list_bids[0]:
                    tob_changed = True
                    self.current_bid = self.list_bids[0] if self.list_bids else None
            if not self.current_ask:
                if not self.list_asks:
                    if self.current_ask is not None:
                        tob_changed = True
                    elif self.current_ask != self.list_asks[0]:
                        tob_changed = True
                        self.current_ask = self.list_asks[0] if self.list_asks else None
            if tob_changed:
                be = self.create_book_event(self.current_bid, self.current_ask)
            if self.ob_2_ts is not None:
                self.ob_2_ts.append(be)
            else:
                return be


