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

    @mock.patch('trading_system.api.blinktrade.clients.BlinkTradeClient.send_request', return_value = {
        u'Status': 200,
        u'Description': u'OK',
        u'Responses': [{
            u'MsgType': u'U3',
            u'4': {u'BRL': 5500000000, u'BRL_locked': 11100000000, u'BTC': 200000000},
            u'ClientID': 90856083,
            u'BalanceReqID': 1467403164
        }]
    })
    def test_it_get_balance(self, _):
        my_current_balance = self.accounts_api.get_balance()
        self.assertIsInstance(my_current_balance, beans.Balance)
        self.assertEqual(my_current_balance.currency, 55.0)
        self.assertEqual(my_current_balance.currency_locked, 111.0)
        self.assertEqual(my_current_balance.btc, 2.0)
        self.assertEqual(my_current_balance.btc_locked, 0.0)

    @mock.patch('trading_system.api.blinktrade.clients.BlinkTradeClient.send_request', return_value = {
        u'Status': 200,
        u'Description': u'OK',
        u'Responses': [{
            u'MsgType': u'U3',
            u'invalid_broker': {u'BTC_locked': 0, u'BRL': 6810428250, u'BRL_locked': 0, u'BTC': 0},
            u'ClientID': 90856083,
            u'BalanceReqID': 1467403164
        }]
    })
    def test_it_get_no_balance(self, _):
        my_current_balance = self.accounts_api.get_balance()
        self.assertIsInstance(my_current_balance, beans.Balance)
        self.assertEqual(my_current_balance.currency, 0.0)
        self.assertEqual(my_current_balance.currency_locked, 0.0)
        self.assertEqual(my_current_balance.btc, 0.0)
        self.assertEqual(my_current_balance.btc_locked, 0.0)
