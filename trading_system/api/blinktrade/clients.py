from blinktrade.clients import AuthClient, OpenClient
from blinktrade import consts as api_consts

from trading_system import consts
from trading_system.api.blinktrade import accounts, markets, orders
from trading_system.api.interfaces import IClient


class BlinkTradeClient(IClient):
    API_VERSION = 'v1'
    ENV_TYPE_TO_SERVER_MAP = {
        consts.Environment.PRODUCTION: 'https://api.blinktrade.com',
        consts.Environment.TEST: 'https://api.testnet.blinktrade.com',
    }

    def __init__(self, environment_type, currency, broker, key, secret_key):
        """
        :type environment_type: basestring
        :type currency: basestring
        :type broker: basestring
        :type key: basestring
        :type secret_key: basestring
        """
        self.environment_type = environment_type
        self.currency = currency
        self.broker = broker
        self.key = key
        self.secret_key = secret_key
        self.environment_server = self.ENV_TYPE_TO_SERVER_MAP[self.environment_type]

        self.account = accounts.BlinkTradeAccountApi(self)
        self.market = markets.BlinkTradeMarketApi(self)
        self.orders = orders.BlinkTradeOrdersApi(self)

        self.open_api = OpenClient(
            api_consts.Environment.PRODUCTION, api_consts.Currency.BRAZILIAN_REAIS, api_consts.Broker.FOXBIT,
        )
        self.auth_api = AuthClient(
            api_consts.Environment.PRODUCTION,
            api_consts.Currency.BRAZILIAN_REAIS,
            api_consts.Broker.FOXBIT,
            key,
            secret_key
        )
