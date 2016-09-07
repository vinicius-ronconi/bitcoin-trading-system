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

    def get_balance(self):
        return self.client.account.get_balance()

if __name__ == '__main__':
    print(ManualTradingSystem().get_balance())
