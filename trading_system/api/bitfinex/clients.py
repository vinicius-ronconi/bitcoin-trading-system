from bitfinex.client import Client, TradeClient
from trading_system import consts
from trading_system.api.bitfinex import accounts, markets, orders
from trading_system.api.interfaces import IClient


class BitfinexClient(IClient):
    ENV_TYPE_TO_SERVER_MAP = {
        consts.Environment.PRODUCTION: 'https://api.bitfinex.com',
        consts.Environment.TEST: 'https://api.testnet.bitfinex.com',
    }

    api = NotImplemented
    trade_api = NotImplemented
    account = NotImplemented
    market = NotImplemented
    orders = NotImplemented

    def __init__(self, environment_type, symbol, key, secret_key):
        """
        :type environment_type: basestring
        :type symbol: basestring
        :type key: basestring
        :type secret_key: basestring
        """
        self.environment_type = self._validate_environment_type(environment_type)
        self.environment_server = self.ENV_TYPE_TO_SERVER_MAP[self.environment_type]

        self.symbol = symbol

        self.key = key
        self.secret_key = secret_key

        self.account = accounts.BitfinexAccountApi(self)
        self.market = markets.BitfinexMarketApi(self)
        self.orders = orders.BitfinexOrdersApi(self)

        self.api = Client()
        self.trade_api = TradeClient(key, secret_key)

    @staticmethod
    def _validate_environment_type(env):
        return env if env in consts.ENVIRONMENTS_CHOICES else consts.Environment.TEST

    @staticmethod
    def get_decimal_value(satoshi):
        if satoshi is None:
            return None
        return float(satoshi) / consts.SATOSHI_PRECISION

    @staticmethod
    def get_satoshi_value(value):
        # TODO: Remove from interface and move to a utils module
        if value is None:
            return None
        return int(value * consts.SATOSHI_PRECISION)