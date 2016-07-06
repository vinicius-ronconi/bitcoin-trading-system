from trading_system.api.clients import BlinkTradeClient
from trading_system.api import consts
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


if __name__ == '__main__':
    print ManualTradingSystem().get_balance()
