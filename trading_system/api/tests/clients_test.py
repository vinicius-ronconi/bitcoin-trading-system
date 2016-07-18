from unittest import TestCase

from trading_system import consts
from trading_system.api.clients import BlinkTradeClient


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

    def test_it_defaults_to_brazilian_test_environment(self):
        client = BlinkTradeClient('invalid type', 'invalid currency', 'invalid broker', 'my_key', 'secret_key')
        self.assertEqual(client.environment_type, consts.Environment.TEST)
        self.assertTrue('testnet' in client.environment_server)
        self.assertEqual(client.currency, consts.Currency.BRAZILIAN_REAIS)
        self.assertEqual(client.broker, consts.Broker.FOXBIT)

    def test_it_converts_satoshi_to_currency(self):
        satoshi = 123456789
        currency = self.client.get_currency_value(satoshi)
        self.assertIsInstance(currency, float)
        self.assertEqual(currency, float(satoshi) / consts.SATOSHI_PRECISION)

    def test_it_returns_none_for_none_satoshi(self):
        satoshi = None
        currency = self.client.get_currency_value(satoshi)
        self.assertIsNone(currency)

    def test_it_converts_currency_to_satoshi(self):
        value = 1234
        satoshi = self.client.get_satoshi_value(value)
        self.assertIsInstance(satoshi, int)
        self.assertEqual(satoshi, int(value * consts.SATOSHI_PRECISION))

    def test_it_returns_none_for_none_value(self):
        value = None
        satoshi = self.client.get_satoshi_value(value)
        self.assertIsNone(satoshi)

    def test_if_creates_an_int_unique_id(self):
        value = self.client.get_unique_id()
        self.assertIsInstance(value, int)
        self.assertGreater(value, 0)
