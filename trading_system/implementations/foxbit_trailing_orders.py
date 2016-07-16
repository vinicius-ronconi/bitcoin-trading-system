from trading_system.api import consts
from trading_system.api.clients import BlinkTradeClient
from trading_system.systems.settings import *
from trading_system.systems.trailing_orders import TrailingOrders


class FoxbitTrailingOrder(object):
    def __init__(self):
        client = BlinkTradeClient(
            consts.Environment.PRODUCTION,
            consts.Currency.BRAZILIAN_REAIS,
            consts.Broker.FOXBIT,
            BLINKTRADE_KEY, BLINKTRADE_SECRET
        )

        self.system = TrailingOrders(client)

    def run(self):
        self.system.run()


if __name__ == '__main__':
    FoxbitTrailingOrder().run()
