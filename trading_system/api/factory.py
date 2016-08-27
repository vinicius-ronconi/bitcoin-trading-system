from trading_system import consts
from trading_system.api.bitfinex.clients import BitfinexClient
from trading_system.api.blinktrade.clients import BlinkTradeClient
from trading_system.systems import settings


class ApiClientFactory(object):
    BITFINEX = 'bitfinex'
    BLINKTRADE = 'blinktrade'

    @staticmethod
    def make_bitfinex_client():
        return BitfinexClient(
            consts.Environment.PRODUCTION,
            consts.Symbol.BTCUSD,
            settings.BITFINEX_KEY,
            settings.BITFINEX_SECRET,
        )

    @staticmethod
    def make_blinktrade_client():
        return BlinkTradeClient(
            consts.Environment.PRODUCTION,
            consts.Currency.BRAZILIAN_REAIS,
            consts.Broker.FOXBIT,
            settings.BLINKTRADE_KEY,
            settings.BLINKTRADE_SECRET,
        )

    def make_client(self, client_type):
        make_client_func = {
            self.BITFINEX: self.make_bitfinex_client,
            self.BLINKTRADE: self.make_blinktrade_client
        }[client_type]
        return make_client_func()
