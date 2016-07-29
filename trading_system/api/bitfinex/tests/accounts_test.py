import mock
from unittest import TestCase

from trading_system import consts
from trading_system.api.bitfinex.accounts import BitfinexAccountApi
from trading_system.api.beans import Balance
from trading_system.api.bitfinex.clients import BitfinexClient


class BitfinexAccountApiTestCase(TestCase):
    accounts = None

    def setUp(self):
        client = BitfinexClient(consts.Environment.PRODUCTION, consts.Symbol.BTCUSD, 'my_key', 'my_secret')
        self.accounts = BitfinexAccountApi(client)

    @mock.patch('bitfinex.client.TradeClient.balances', return_value=[
        {
            "type": "deposit",
            "currency": "btc",
            "amount": "1.0",
            "available": "1.0"
        }, {
            "type": "deposit",
            "currency": "usd",
            "amount": "100.0",
            "available": "100.0"
        }, {
            "type": "exchange",
            "currency": "btc",
            "amount": "2",
            "available": "1"
        }, {
            "type": "exchange",
            "currency": "usd",
            "amount": "200",
            "available": "200"
        }, {
            "type": "trading",
            "currency": "btc",
            "amount": "3",
            "available": "3"
        }, {
            "type": "trading",
            "currency": "usd",
            "amount": "300",
            "available": "300"
        }
    ])
    def test_it_get_balance(self, _):
        my_current_balance = self.accounts.get_balance()
        self.assertIsInstance(my_current_balance, Balance)
        self.assertEqual(my_current_balance.currency, 200.0)
        self.assertEqual(my_current_balance.currency_locked, 0.0)
        self.assertEqual(my_current_balance.btc, 1.0)
        self.assertEqual(my_current_balance.btc_locked, 1.0)
