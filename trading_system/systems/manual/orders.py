from trading_system import consts
from trading_system.api.bitfinex.clients import BitfinexClient
from trading_system.settings import BITFINEX_KEY, BITFINEX_SECRET


class ManualTradingSystem(object):
    def __init__(self):
        self.client = BitfinexClient(
            consts.Environment.PRODUCTION,
            consts.Symbol.BTCUSD,
            BITFINEX_KEY,
            BITFINEX_SECRET,
        )

    def get_pending_orders(self, page, page_size):
        return self.client.orders.get_pending_orders(page, page_size)

    def buy_bitcoins_with_limited_order(self, price, quantity):
        return self.client.orders.buy_bitcoins_with_limited_order(price, quantity)

    def buy_bitcoins_with_market_order(self, quantity):
        return self.client.orders.buy_bitcoins_with_market_order(quantity)

    def sell_bitcoins_with_limited_order(self, price, quantity):
        return self.client.orders.sell_bitcoins_with_limited_order(price, quantity)

    def sell_bitcoins_with_market_order(self, quantity):
        return self.client.orders.sell_bitcoins_with_market_order(quantity)

    def cancel_order(self, order_id):
        return self.client.orders.cancel_order(order_id)

if __name__ == '__main__':
    print(ManualTradingSystem().get_pending_orders(1, 10))
    print(ManualTradingSystem().sell_bitcoins_with_limited_order(578.20, 0.215))
    print(ManualTradingSystem().buy_bitcoins_with_limited_order(575.0, 0.215))
    print(ManualTradingSystem().cancel_order(1011770681))
    print(ManualTradingSystem().sell_bitcoins_with_market_order(0.2182))
    print(ManualTradingSystem().buy_bitcoins_with_market_order(0.02))
