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

    def get_past_orders(self, page, page_size):
        return self.client.orders.get_executed_orders(page, page_size)

if __name__ == '__main__':
    print(ManualTradingSystem().get_pending_orders(1, 10))
    print(ManualTradingSystem().get_past_orders(1, 10))
