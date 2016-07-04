from unittest import TestCase

import mock

from trading_system.api import beans
from trading_system.api import consts
from trading_system.api import exceptions
from trading_system.api.orders import BlinkTradeOrdersApi


class BlinkTradeOrdersApiTestCase(TestCase):
    def setUp(self):
        self.client = mock.Mock()
        self.client.environment_type = consts.Environment.PRODUCTION
        self.client.environment_server = 'http://www.bitcoin_exchange.com'
        self.client.currency = consts.Currency.BRAZILIAN_REAIS
        self.client.broker = consts.Broker.FOXBIT
        self.client.key = 'my_key'
        self.client.secret_key = 'my_secret_key'

        self.orders_api = BlinkTradeOrdersApi(self.client)

    def test_it_places_a_buy_order(self):
        self.client.send_request.return_value = {
            u'Status': 200,
            u'Description': u'OK',
            u'Responses': [
                {
                    u'OrderID': 1459144180001,
                    u'ExecID': 202294,
                    u'ExecType': u'0',
                    u'OrdStatus': u'0',
                    u'CumQty': 0,
                    u'Symbol': u'BTCBRL',
                    u'OrderQty': 3130000,
                    u'LastShares': 0,
                    u'LastPx': 0,
                    u'CxlQty': 0,
                    u'TimeInForce': u'1',
                    u'LeavesQty': 3130000,
                    u'MsgType': u'8',
                    u'ExecSide': u'1',
                    u'OrdType': u'2',
                    u'Price': 217500000000,
                    u'Side': u'1',
                    u'ClOrdID': 1467403664,
                    u'AvgPx': 0
                },
                {
                    u'MsgType': u'U3',
                    u'4': {u'BRL_locked': 6807750000},
                    u'ClientID': 90856083
                }
            ]
        }
        order_response = self.orders_api.buy_bitcoins(consts.OrderType.LIMITED_ORDER, price=2175, quantity=0.0313)
        self.assertIsInstance(order_response, list)
        self.assertIsInstance(order_response[0], beans.PlacedOrder)
        self.assertIsInstance(order_response[1], beans.Balance)

    def test_it_does_not_accept_an_order_with_too_small_value(self):
        self.client.send_request.return_value = {
            u'Status': 200,
            u'Description': u'OK',
            u'Responses': [
                {
                    u'OrderID': None,
                    u'TimeInForce': u'1',
                    u'ExecID': None,
                    u'ExecType': u'8',
                    u'OrdStatus': u'8',
                    u'CumQty': 0,
                    u'Price': 1000000,
                    u'Symbol': u'BTCBRL',
                    u'OrderQty': 10,
                    u'LastShares': 0,
                    u'LastPx': 0,
                    u'CxlQty': 0,
                    u'Volume': 0,
                    u'LeavesQty': 0,
                    u'MsgType': u'8',
                    u'ExecSide': u'1',
                    u'OrdType': u'2',
                    u'OrdRejReason': u'3',
                    u'Side': u'1',
                    u'ClOrdID': 1467406237,
                    u'AvgPx': 0
                }
            ]
        }
        self.assertRaises(
            exceptions.OrderRejectedException,
            self.orders_api.buy_bitcoins,
            order_type=consts.OrderType.LIMITED_ORDER,
            price=0.01,
            quantity=0.00000001,
        )

    def test_it_places_a_sell_order(self):
        self.client.send_request.return_value = {
            u'Status': 200,
            u'Description': u'OK',
            u'Responses': [
                {
                    u'OrderID': 1459144180001,
                    u'ExecID': 202294,
                    u'ExecType': u'0',
                    u'OrdStatus': u'0',
                    u'CumQty': 0,
                    u'Symbol': u'BTCBRL',
                    u'OrderQty': 3130000,
                    u'LastShares': 0,
                    u'LastPx': 0,
                    u'CxlQty': 0,
                    u'TimeInForce': u'1',
                    u'LeavesQty': 3130000,
                    u'MsgType': u'8',
                    u'ExecSide': u'1',
                    u'OrdType': u'2',
                    u'Price': 217500000000,
                    u'Side': u'2',
                    u'ClOrdID': 1467403664,
                    u'AvgPx': 0
                },
                {
                    u'MsgType': u'U3',
                    u'4': {u'BRL_locked': 6807750000},
                    u'ClientID': 90856083
                }
            ]
        }
        order_response = self.orders_api.sell_bitcoins(consts.OrderType.LIMITED_ORDER, price=2175, quantity=0.0313)
        self.assertIsInstance(order_response, list)
        self.assertIsInstance(order_response[0], beans.PlacedOrder)
        self.assertIsInstance(order_response[1], beans.Balance)

    def test_it_cancels_an_order(self):
        self.client.send_request.return_value = {
            u'Status': 200,
            u'Description': u'OK',
            u'Responses': [
                {
                    u'OrderID': 1459144180001,
                    u'ExecID': 202543,
                    u'ExecType': u'4',
                    u'OrdStatus': u'4',
                    u'CumQty': 0,
                    u'Symbol': u'BTCBRL',
                    u'OrderQty': 3130000,
                    u'LastShares': 0,
                    u'LastPx': 0,
                    u'CxlQty': 3130000,
                    u'TimeInForce': u'1',
                    u'LeavesQty': 0,
                    u'MsgType': u'8',
                    u'ExecSide': u'1',
                    u'OrdType': u'2',
                    u'Price': 217500000000,
                    u'Side': u'1',
                    u'ClOrdID': u'1467403664',
                    u'AvgPx': 0
                },
                {
                    u'MsgType': u'U3',
                    u'4': {u'BRL_locked': 0},
                    u'ClientID': 90856083
                }
            ]
        }
        order_response = self.orders_api.cancel_order(order_id='1467403664')
        self.assertIsInstance(order_response, list)
        self.assertIsInstance(order_response[0], beans.PlacedOrder)
        self.assertIsInstance(order_response[1], beans.Balance)

