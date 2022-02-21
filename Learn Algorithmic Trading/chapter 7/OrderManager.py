class OrderManager:
    def __init__(self, ts_2_om=None, om_2_ts=None, om_2_gw=None, gw_2_om=None):
        self.orders = []
        self.order_id = 0
        self.ts_2_om = ts_2_om
        self.om_2_gw = om_2_gw
        self.gw_2_om = gw_2_om
        self.om_2_ts = om_2_ts

    def handle_input_from_ts(self):
        """
        Checks whether ts_2_om channel is created. If the channel has not been created, it means the class is used
        for unit testing only.
        :return:
        """
        if self.ts_2_om is not None:
            if len(self.ts_2_om) > 0:
                self.handle_order_from_trading_strategy(self.ts_2_om.popleft())
        else:
            print("Simulation mode")

    def handle_order_from_trading_strategy(self, order):
        if self.check_order_valid(order):
            order = self.create_new_order(order).copy()
            self.orders.append(order)
            if self.om_2_gw is None:
                print("Simulation mode")
            else:
                self.om_2_gw.append(order.copy())

    def handle_input_from_market(self):
        """
        Checks whether the gw_2_om channel exists.
        :return:
        """
        if self.gw_2_om is not None:
            if len(self.gw_2_om) > 0:
                self.handle_order_from_gateway(self.gw_2_om.popleft())
        else:
            print("Simulation mode")

    def handle_order_from_gateway(self, order_update):
        """
        Lookup list of orders created by handle_order_from_trading_strategy function.
        If the market response corresponds to an order in the list, it means the market response is valid.
        If the market response does not find a specific order, it means there is a problem between the trading system
        and market.
        :param order_update:
        :return:
        """
        order = self.lookup_order_by_id(order_update["id"])
        if order is not None:
            order["status"] = order_update["status"]
            if self.om_2_ts is not None:
                self.om_2_ts.append(order.copy())
            else:
                print("Simulation mode")
            self.clean_traded_orders()

        else:
            print("Order not found")

    def check_order_valid(self, order):
        if order["quantity"] < 0 or order["price"] < 0:
            return False
        return True

    def create_new_order(self, order):
        """
        Creates an order based on the order sent by the trading strategy, which has a unique order id.
        :return:
        """
        self.order_id += 1
        neworder = {
            "id": self.order_id,
            "price": order["price"],
            "quantity": order["quantity"],
            "side": order["side"],
            "status": "new",
            "action": "New"
        }
        return neworder

    def lookup_order_by_id(self, id):
        """
        Looks up an order by its id.
        :param id:
        :return:
        """
        for i in range(len(self.orders)):
            if self.orders[i]["id"] == id:
                return self.order[i]
        return None

    def clean_traded_orders(self):
        """
        Removes all orders that have been filled from the list of orders.
        :return:
        """
        order_offsets = []
        for k in range(len(self.orders)):
            if self.order[k]["status"] == "filled":
                order_offsets.append(self.order[k])
        if len(order_offsets):
            for k in sorted(order_offsets, reverse=True):
                del (self.orders[k])

    
