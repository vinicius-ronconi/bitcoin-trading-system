from unittest import TestCase

from trading_system import consts
from trading_system.api.blinktrade.clients import BlinkTradeClient


class EnvironmentTestCase(TestCase):
    def setUp(self):
        self.env_type = consts.Environment.PRODUCTION
        self.currency = consts.Currency.BRAZILIAN_REAIS
        self.broker = consts.Broker.FOXBIT
        self.client = BlinkTradeClient(self.env_type, self.currency, self.broker, 'my_key', 'secret_key')

    def test_it_creates_a_blinktrade_client_in_production_environment(self):
        self.assertEqual(self.client.environment_type, self.env_type)
        self.assertFalse('testnet' in self.client.environment_server)
        self.assertEqual(self.client.currency, self.currency)
        self.assertEqual(self.client.broker, self.broker)
        self.assertIsNotNone(self.client.account)
        self.assertIsNotNone(self.client.market)
        self.assertIsNotNone(self.client.orders)
