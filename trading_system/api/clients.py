import datetime
import hashlib
import hmac
import time

import requests

from trading_system import consts
from trading_system.api import (
    accounts,
    markets,
    orders,
)
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
        self.environment_type = self._validate_environment_type(environment_type)
        self.environment_server = self.ENV_TYPE_TO_SERVER_MAP[self.environment_type]

        self.currency = self._validate_currency(currency)
        self.broker = self._validate_broker(broker)

        self.key = key
        self.secret_key = secret_key

        self.account = accounts.BlinkTradeAccountApi(self)
        self.market = markets.BlinkTradeMarketApi(self)
        self.orders = orders.BlinkTradeOrdersApi(self)

    @staticmethod
    def _validate_environment_type(env):
        return env if env in consts.ENVIRONMENTS_CHOICES else consts.Environment.TEST

    @staticmethod
    def _validate_currency(currency):
        return currency if currency in consts.CURRENCIES_CHOICES else consts.Currency.BRAZILIAN_REAIS

    @staticmethod
    def _validate_broker(broker):
        return broker if broker in consts.BROKERS_CHOICES else consts.Broker.FOXBIT

    @staticmethod
    def get_unique_id():
        return int(time.time())

    @staticmethod
    def get_currency_value(satoshi):
        if satoshi is None:
            return None
        return float(satoshi) / consts.SATOSHI_PRECISION

    @staticmethod
    def get_satoshi_value(value):
        if value is None:
            return None
        return long(value * consts.SATOSHI_PRECISION)

    def send_request(self, msg):
        dt = datetime.datetime.now()
        nonce = str(
            int((time.mktime(dt.timetuple()) + dt.microsecond / float(consts.NONCE_PRECISION)) * consts.NONCE_PRECISION)
        )
        signature = hmac.new(self.secret_key, nonce, digestmod=hashlib.sha256).hexdigest()

        headers = {
            'user-agent': 'blinktrade_tools/0.1',
            'Content-Type': 'application/json',
            'APIKey': self.key,
            'Nonce': nonce,
            'Signature': signature
        }
        url = '{domain}/tapi/{version}/message'.format(
            domain=self.environment_server, version=self.API_VERSION
        )
        return requests.post(url, json=msg, verify=True, headers=headers).json()
