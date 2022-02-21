class MarketSimulator:
    def __init__(self, om_2_gw=None, gw_2_om=None):
        self.orders = []
        self.om_2_gw = om_2_gw
        self.gw_2_om = gw_2_om

    def lookup_orders(self, order):
        count = 0
        for ord in self.orders:
            if ord["id"] == order["od"]:
                return ord, count
            count += 1
        return None, None

    def handle_order_from_gw(self):
        """
        Collects order from the gateway through the om_2_gw channel.
        :return:
        """
        if self.om_2_gw is not None:
            if len(self.om_2_gw) > 0:
                self.handle_order(self.om_2_gw.popleft())
        else:
            print("Simulation mode")

    def handle_order(self, order):
        """
        Accepts any new orders. If an order already has the same order id, the order will be dropped.
        Custom logic to be programmed here to adapt to your trading.
        :param order:
        :return:
        """
        ord, offset = self.lookup_orders(order)
        if ord is None:
            if order["action"] == "New":
                order["status"] = "accepted"
                self.orders.append(order)
                if self.gw_2_om is not None:
                    self.gw_2_om.append(order.copy())
                else:
                    print("Simulation mode")
                return

            elif order["action"] == "Cancel" or order["action"] == "Amend":
                print("Order id - not found - Rejection")
                if self.gw_2_om is not None:
                    self.gw_2_om.append(order.copy())
                else:
                    print("Simulation mode")
                return

        elif ord is not None:
            if order["action"] == "New":
                print("Duplicate order id - Rejection")
                return
            elif order["action"] == "Cancel":
                ord["status"] == "cancelled"
                if self.gw_2_om is not None:
                    self.gw_2_om.append(ord.copy())
                else:
                    print("Simulation mode")
                del (self.orders[offset])
                print("Order cancelled")
            elif order["action"] == "Amend":
                ord["status"] = "accepted"
                if self.gw_2_om is not None:
                    self.gw_2_om.append(ord.copy())
                else:
                    print("Simulation mode")
                print("Order amended")

    def fill_all_orders(self):
        orders_to_be_removed = []
        for index, order in enumerate(self.orders):
            order["status"] = "filled"
            orders_to_be_removed.append(index)
            if self.gw_2_om is not None:
                self.gw_2_om.append(order.copy())
            else:
                print("Simulation mode")
        for i in sorted(orders_to_be_removed, reverse=True):
            del(self.orders[i])

