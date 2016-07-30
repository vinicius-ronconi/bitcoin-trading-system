from trading_system import consts
from trading_system.api.bitfinex.clients import BitfinexClient
from trading_system.systems.executor import SystemExecutor
from trading_system.systems.settings import *
from trading_system.systems.trailing_orders import TrailingOrders


class BitfinexTrailingOrder(object):
    def __init__(self):
        # TODO Create abstract factory
        client = BitfinexClient(
            consts.Environment.PRODUCTION,
            consts.Symbol.BTCUSD,
            BITFINEX_KEY,
            BITFINEX_SECRET,
        )

        self.system = TrailingOrders(client)

    def run(self):
        executor = SystemExecutor(self.system, interval=3)
        executor.execute()

if __name__ == '__main__':
    BitfinexTrailingOrder().run()
