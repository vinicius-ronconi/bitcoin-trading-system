from trading_system import consts
from trading_system.api.blinktrade.clients import BlinkTradeClient
from trading_system.systems.executor import SystemExecutor
from trading_system.systems.settings import *
from trading_system.systems.trailing_orders import TrailingOrders


class FoxbitTrailingOrder(object):
    def __init__(self):
        # TODO Create abstract factory
        client = BlinkTradeClient(
            consts.Environment.PRODUCTION,
            consts.Currency.BRAZILIAN_REAIS,
            consts.Broker.FOXBIT,
            BLINKTRADE_KEY, BLINKTRADE_SECRET
        )

        self.system = TrailingOrders(client)

    def run(self):
        executor = SystemExecutor(self.system, interval=3)
        executor.execute()

if __name__ == '__main__':
    FoxbitTrailingOrder().run()
