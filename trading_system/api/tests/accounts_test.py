from unittest import TestCase

import mock

from trading_system.api import beans
from trading_system.api import consts
from trading_system.api.accounts import BlinkTradeAccountApi


class AccountsTestCase(TestCase):
    def setUp(self):
        self.client = mock.Mock()
        self.client.environment_type = consts.Environment.PRODUCTION
        self.client.environment_server = 'http://www.bitcoin_exchange.com'
        self.client.currency = consts.Currency.BRAZILIAN_REAIS
        self.client.broker = consts.Broker.FOXBIT
        self.client.key = 'my_key'
        self.client.secret_key = 'my_secret_key'

        self.accounts_api = BlinkTradeAccountApi(self.client)

    def test_it_get_balance(self):
        self.client.send_request.return_value = {
            u'Status': 200,
            u'Description': u'OK',
            u'Responses': [{
                u'MsgType': u'U3',
                u'4': {u'BRL': 6810428250, u'BRL_locked': 10000000000, u'BTC': 200000000},
                u'ClientID': 90856083,
                u'BalanceReqID': 1467403164
            }]
        }

        balance = self.accounts_api.get_balance()
        self.assertIsInstance(balance, beans.Balance)

    def test_it_get_no_balance(self):
        self.client.send_request.return_value = {
            u'Status': 200,
            u'Description': u'OK',
            u'Responses': [{
                u'MsgType': u'U3',
                u'4': {u'BTC_locked': 0, u'BRL': 6810428250, u'BRL_locked': 0, u'BTC': 0},
                u'ClientID': 90856083,
                u'BalanceReqID': 1467403164
            }]
        }

        balance = self.accounts_api.get_balance()
        self.assertIsInstance(balance, beans.Balance)
