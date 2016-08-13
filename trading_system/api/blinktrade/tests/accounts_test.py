from unittest import TestCase

import mock

from trading_system import consts
from trading_system.api import beans
from trading_system.api.blinktrade.accounts import BlinkTradeAccountApi
from trading_system.api.blinktrade.clients import BlinkTradeClient


class AccountsTestCase(TestCase):
    def setUp(self):
        client = BlinkTradeClient(
            consts.Environment.PRODUCTION,
            consts.Currency.BRAZILIAN_REAIS,
            consts.Broker.FOXBIT,
            'my_key',
            'my_secret',
        )
        self.accounts_api = BlinkTradeAccountApi(client)

    @mock.patch('blinktrade.clients.AuthClient.get_balance', return_value={
        u'BRL': 1.0,
        u'BRL_locked': 2.0,
        u'BTC': 3.0,
        u'BTC_locked': 4.0,
    })
    def test_it_get_balance(self, _):
        my_current_balance = self.accounts_api.get_balance()
        self.assertIsInstance(my_current_balance, beans.Balance)
        self.assertEqual(my_current_balance.currency, 1.0)
        self.assertEqual(my_current_balance.currency_locked, 2.0)
        self.assertEqual(my_current_balance.btc, 3.0)
        self.assertEqual(my_current_balance.btc_locked, 4.0)

    @mock.patch('blinktrade.clients.AuthClient.get_balance', return_value={})
    def test_it_get_no_balance(self, _):
        my_current_balance = self.accounts_api.get_balance()
        self.assertIsInstance(my_current_balance, beans.Balance)
        self.assertEqual(my_current_balance.currency, 0.0)
        self.assertEqual(my_current_balance.currency_locked, 0.0)
        self.assertEqual(my_current_balance.btc, 0.0)
        self.assertEqual(my_current_balance.btc_locked, 0.0)
