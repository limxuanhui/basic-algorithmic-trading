# Randomly generate liquidities

from random import randrange, sample, seed

class LiquidityProvider:
    def __init__(self, lp_2_gateway=None):
        self.orders = []
        self.order_id = 0
        self.lp_2_gateway = lp_2_gateway
        seed(0)

    def lookup_orders(self, id):
        """
        Look up orders in the list of orders
        :param id: order id
        :return: order, count
        """
        count = 0
        for order in  self.orders:
            if order["id"] == id:
                return order, count
            count += 1
        return None, None

    def insert_manual_order(self, order):
        if self.lp_2_gateway is None:
            print("Simulation mode")
            return order
        self.lp_2_gateway.append(order.copy())

    def generate_random_order(self):
        """
        Generate orders randomly. New, Modify or Delete orders.
        :return:
        """
        price = randrange(8, 12)
        quantity = randrange(1, 10) * 100
        side = sample(["buy", "sell"], 1)[0]
        order_id = randrange(0, self.order_id + 1)
        order, _ = self.lookup_orders(order_id)

        new_order = False
        if order is None:
            action = "new"
            new_order = True
        else:
            action = sample(["modify", "delete"], 1)[0]

        order = {
            "id": self.order_id,
            "price": price,
            "quantity": quantity,
            "side": side,
            "action": action
        }
        print(order)

        if not new_order:
            self.order_id += 1
            self.orders.append(order)

        if not self.lp_2_gateway:
            print("Simulation mode")
            return order

        self.lp_2_gateway.append(order.copy())
