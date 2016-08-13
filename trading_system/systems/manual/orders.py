from trading_system import consts
from trading_system.api.bitfinex.clients import BitfinexClient
from trading_system.systems.settings import *


class ManualTradingSystem(object):
    def __init__(self):
        self.client = BitfinexClient(
            consts.Environment.PRODUCTION,
            consts.Symbol.BTCUSD,
            BITFINEX_KEY, BITFINEX_SECRET,
        )

    def get_pending_orders(self, page, page_size):
        return self.client.orders.get_pending_orders(page, page_size)

    def sell_bitcoins(self):
        return self.client.orders.sell_bitcoins_with_limited_order(price=659.20, quantity=0.249275)

if __name__ == '__main__':
    print (ManualTradingSystem().sell_bitcoins())
    print(ManualTradingSystem().get_pending_orders(1, 10))
