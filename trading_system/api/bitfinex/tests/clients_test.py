from unittest import TestCase

from trading_system import consts
from trading_system.api.bitfinex.clients import BitfinexClient


class EnvironmentTestCase(TestCase):
    def test_it_creates_a_blinktrade_client_in_production_environment(self):
        self.env_type = consts.Environment.PRODUCTION
        self.symbol = consts.Symbol.BTCUSD
        self.client = BitfinexClient(self.env_type, self.symbol, 'my_key', 'my_secret')

        self.assertEqual(self.client.environment_type, self.env_type)
        self.assertFalse('testnet' in self.client.environment_server)
        self.assertEqual(self.client.symbol, self.symbol)
        self.assertIsNotNone(self.client.account)
        self.assertIsNotNone(self.client.market)
        self.assertIsNotNone(self.client.orders)
