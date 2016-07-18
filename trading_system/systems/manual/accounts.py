from trading_system import consts
from trading_system.api.clients import BlinkTradeClient
from trading_system.systems.settings import *


class ManualTradingSystem(object):
    def __init__(self):
        self.client = BlinkTradeClient(
            consts.Environment.PRODUCTION,
            consts.Currency.BRAZILIAN_REAIS,
            consts.Broker.FOXBIT,
            BLINKTRADE_KEY, BLINKTRADE_SECRET,
        )

    def get_balance(self):
        return self.client.account.get_balance()

    def get_pending_orders(self):
        return self.client.orders.get_pending_orders(0, 100)

if __name__ == '__main__':
    print(ManualTradingSystem().get_balance())
    print(ManualTradingSystem().get_pending_orders())
