from unittest import TestCase

import mock

from trading_system import consts
from trading_system.api import beans
from trading_system.api.blinktrade.clients import BlinkTradeClient
from trading_system.api.blinktrade.orders import BlinkTradeOrdersApi


class OrdersTestCase(TestCase):
    orders_api = NotImplemented

    def setUp(self):
        client = BlinkTradeClient(
            consts.Environment.PRODUCTION,
            consts.Currency.BRAZILIAN_REAIS,
            consts.Broker.FOXBIT,
            'my_key',
            'my_secret',
        )
        self.orders_api = BlinkTradeOrdersApi(client)

    @mock.patch('blinktrade.clients.AuthClient.buy_bitcoins_with_limited_order', mock.Mock(return_value=[
        {
            u'OrderID': 1459144180001,
            u'ExecID': 202294,
            u'ExecType': u'0',
            u'OrdStatus': u'0',
            u'CumQty': 0,
            u'Symbol': u'BTCBRL',
            u'OrderQty': 0.03130000,
            u'LastShares': 0,
            u'LastPx': 0,
            u'CxlQty': 0,
            u'TimeInForce': u'1',
            u'LeavesQty': 0.03130000,
            u'MsgType': u'8',
            u'ExecSide': u'1',
            u'OrdType': u'2',
            u'Price': 2175.0,
            u'Side': u'1',
            u'ClOrdID': 1467403664,
            u'AvgPx': 0
        },
        {
            u'BRL': 1.0,
            u'BRL_locked': 2.0,
            u'BTC': 3.0,
            u'BTC_locked': 4.0,
        }
    ]))
    def test_it_places_a_limited_buy_order(self):
        order_response = self.orders_api.buy_bitcoins_with_limited_order(price=2175, quantity=0.0313)
        self.assertIsInstance(order_response, list)
        self.assertIsInstance(order_response[0], beans.PlacedOrder)
        self.assertEqual(order_response[0].order_id, '1459144180001')
        self.assertEqual(order_response[0].exec_id, '202294')
        self.assertEqual(order_response[0].exec_type, '0')
        self.assertEqual(order_response[0].order_status, '0')
        self.assertEqual(order_response[0].price, 2175.0)
        self.assertEqual(order_response[0].symbol, 'BTCBRL')
        self.assertEqual(order_response[0].amount, 0.0313)
        self.assertEqual(order_response[0].message_type, '8')
        self.assertEqual(order_response[0].side, '1')
        self.assertEqual(order_response[0].client_order_id, '1467403664')
        self.assertIsNone(order_response[0].order_rejection_reason)

        self.assertIsInstance(order_response[1], beans.Balance)
        self.assertEqual(order_response[1].currency_locked, 2.0)

    @mock.patch('blinktrade.clients.AuthClient.buy_bitcoins_with_market_order', mock.Mock(return_value=[
        {
            u'OrderID': 1459144180001,
            u'ExecID': 202294,
            u'ExecType': u'0',
            u'OrdStatus': u'0',
            u'CumQty': 0,
            u'Symbol': u'BTCBRL',
            u'OrderQty': 0.03130000,
            u'LastShares': 0,
            u'LastPx': 0,
            u'CxlQty': 0,
            u'TimeInForce': u'1',
            u'LeavesQty': 0.03130000,
            u'MsgType': u'8',
            u'ExecSide': u'1',
            u'OrdType': u'1',
            u'Price': 2175.0,
            u'Side': u'1',
            u'ClOrdID': 1467403664,
            u'AvgPx': 0
        },
        {
            u'BRL': 1.0,
            u'BRL_locked': 2.0,
            u'BTC': 3.0,
            u'BTC_locked': 4.0,
        }
    ]))
    def test_it_places_a_market_buy_order(self):
        order_response = self.orders_api.buy_bitcoins_with_market_order(quantity=0.0313)
        self.assertIsInstance(order_response, list)
        self.assertIsInstance(order_response[0], beans.PlacedOrder)
        self.assertEqual(order_response[0].order_id, '1459144180001')
        self.assertEqual(order_response[0].exec_id, '202294')
        self.assertEqual(order_response[0].exec_type, '0')
        self.assertEqual(order_response[0].order_status, '0')
        self.assertEqual(order_response[0].price, 2175.0)
        self.assertEqual(order_response[0].symbol, 'BTCBRL')
        self.assertEqual(order_response[0].amount, 0.0313)
        self.assertEqual(order_response[0].message_type, '8')
        self.assertEqual(order_response[0].side, '1')
        self.assertEqual(order_response[0].client_order_id, '1467403664')
        self.assertIsNone(order_response[0].order_rejection_reason)

        self.assertIsInstance(order_response[1], beans.Balance)
        self.assertEqual(order_response[1].currency_locked, 2.0)

    @mock.patch('blinktrade.clients.AuthClient.sell_bitcoins_with_limited_order', mock.Mock(return_value=[
        {
            u'OrderID': 1459144180001,
            u'ExecID': 202294,
            u'ExecType': u'0',
            u'OrdStatus': u'0',
            u'CumQty': 0,
            u'Symbol': u'BTCBRL',
            u'OrderQty': 0.03130000,
            u'LastShares': 0,
            u'LastPx': 0,
            u'CxlQty': 0,
            u'TimeInForce': u'1',
            u'LeavesQty': 0.03130000,
            u'MsgType': u'8',
            u'ExecSide': u'1',
            u'OrdType': u'2',
            u'Price': 2175.0,
            u'Side': u'2',
            u'ClOrdID': 1467403664,
            u'AvgPx': 0
        },
        {
            u'BRL': 1.0,
            u'BRL_locked': 2.0,
            u'BTC': 3.0,
            u'BTC_locked': 4.0
        }
    ]))
    def test_it_places_a_limited_sell_order(self):
        order_response = self.orders_api.sell_bitcoins_with_limited_order(price=2175, quantity=0.0313)
        self.assertIsInstance(order_response, list)
        self.assertIsInstance(order_response[0], beans.PlacedOrder)
        self.assertEqual(order_response[0].order_id, '1459144180001')
        self.assertEqual(order_response[0].exec_id, '202294')
        self.assertEqual(order_response[0].exec_type, '0')
        self.assertEqual(order_response[0].order_status, '0')
        self.assertEqual(order_response[0].price, 2175.0)
        self.assertEqual(order_response[0].symbol, 'BTCBRL')
        self.assertEqual(order_response[0].amount, 0.0313)
        self.assertEqual(order_response[0].message_type, '8')
        self.assertEqual(order_response[0].side, '2')
        self.assertEqual(order_response[0].client_order_id, '1467403664')
        self.assertIsNone(order_response[0].order_rejection_reason)

        self.assertIsInstance(order_response[1], beans.Balance)
        self.assertEqual(order_response[1].currency_locked, 2.0)

    @mock.patch('blinktrade.clients.AuthClient.sell_bitcoins_with_market_order', mock.Mock(return_value=[
        {
            u'OrderID': 1459144180001,
            u'ExecID': 202294,
            u'ExecType': u'0',
            u'OrdStatus': u'0',
            u'CumQty': 0,
            u'Symbol': u'BTCBRL',
            u'OrderQty': 0.03130000,
            u'LastShares': 0,
            u'LastPx': 0,
            u'CxlQty': 0,
            u'TimeInForce': u'1',
            u'LeavesQty': 0.03130000,
            u'MsgType': u'8',
            u'ExecSide': u'1',
            u'OrdType': u'1',
            u'Price': 2175.0,
            u'Side': u'2',
            u'ClOrdID': 1467403664,
            u'AvgPx': 0
        },
        {
            u'BRL': 1.0,
            u'BRL_locked': 2.0,
            u'BTC': 3.0,
            u'BTC_locked': 4.0
        }
    ]))
    def test_it_places_a_market_sell_order(self):
        order_response = self.orders_api.sell_bitcoins_with_market_order(quantity=0.0313)
        self.assertIsInstance(order_response, list)
        self.assertIsInstance(order_response[0], beans.PlacedOrder)
        self.assertEqual(order_response[0].order_id, '1459144180001')
        self.assertEqual(order_response[0].exec_id, '202294')
        self.assertEqual(order_response[0].exec_type, '0')
        self.assertEqual(order_response[0].order_status, '0')
        self.assertEqual(order_response[0].price, 2175.0)
        self.assertEqual(order_response[0].symbol, 'BTCBRL')
        self.assertEqual(order_response[0].amount, 0.0313)
        self.assertEqual(order_response[0].message_type, '8')
        self.assertEqual(order_response[0].side, '2')
        self.assertEqual(order_response[0].client_order_id, '1467403664')
        self.assertIsNone(order_response[0].order_rejection_reason)

        self.assertIsInstance(order_response[1], beans.Balance)
        self.assertEqual(order_response[1].currency_locked, 2.0)

    @mock.patch('blinktrade.clients.AuthClient.cancel_order', mock.Mock(return_value=[
        {
            u'OrderID': 1459144180001,
            u'ExecID': 202543,
            u'ExecType': u'4',
            u'OrdStatus': u'4',
            u'CumQty': 0,
            u'Symbol': u'BTCBRL',
            u'OrderQty': 0.03130000,
            u'LastShares': 0,
            u'LastPx': 0,
            u'CxlQty': 0,
            u'TimeInForce': u'1',
            u'LeavesQty': 0.03130000,
            u'MsgType': u'8',
            u'ExecSide': u'1',
            u'OrdType': u'2',
            u'Price': 2175.0,
            u'Side': u'1',
            u'ClOrdID': 1467403664,
            u'AvgPx': 0
        },
        {
            u'BRL': 1.0,
            u'BRL_locked': 2.0,
            u'BTC': 3.0,
            u'BTC_locked': 4.0,
        }

    ]))
    def test_it_cancels_an_order(self):
        order_response = self.orders_api.cancel_order(order_id='1467403664')
        self.assertIsInstance(order_response, list)
        self.assertIsInstance(order_response[0], beans.PlacedOrder)
        self.assertEqual(order_response[0].order_id, '1459144180001')
        self.assertEqual(order_response[0].exec_id, '202543')
        self.assertEqual(order_response[0].exec_type, '4')
        self.assertEqual(order_response[0].order_status, '4')
        self.assertEqual(order_response[0].price, 2175.0)
        self.assertEqual(order_response[0].symbol, 'BTCBRL')
        self.assertEqual(order_response[0].amount, 0.0313)
        self.assertEqual(order_response[0].message_type, '8')
        self.assertEqual(order_response[0].side, '1')
        self.assertEqual(order_response[0].client_order_id, '1467403664')
        self.assertIsNone(order_response[0].order_rejection_reason)

        self.assertIsInstance(order_response[1], beans.Balance)
        self.assertEqual(order_response[1].currency_locked, 2.0)

    @mock.patch('blinktrade.clients.AuthClient.get_pending_orders', mock.Mock(return_value=[
        {
            u'OrderID': 1459144180001,
            u'OrdStatus': u'0',
            u'CumQty': 0,
            u'Symbol': u'BTCBRL',
            u'OrderQty': 0.03130000,
            u'LastShares': 0,
            u'LastPx': 0,
            u'CxlQty': 0,
            u'TimeInForce': u'1',
            u'LeavesQty': 0.03130000,
            u'ExecSide': u'1',
            u'OrdType': u'2',
            u'Price': 2175.0,
            u'Side': u'1',
            u'ClOrdID': 1467403664,
            u'AvgPx': 0
        }
    ]))
    def test_it_gets_pending_orders(self):
        order_response = self.orders_api.get_pending_orders(page=0, page_size=100)
        self.assertIsInstance(order_response, list)
        self.assertIsInstance(order_response[0], beans.PlacedOrder)
        self.assertEqual(order_response[0].order_id, '1459144180001')
        self.assertEqual(order_response[0].order_status, '0')
        self.assertEqual(order_response[0].price, 2175.0)
        self.assertEqual(order_response[0].symbol, 'BTCBRL')
        self.assertEqual(order_response[0].amount, 0.0313)
        self.assertEqual(order_response[0].side, '1')
        self.assertEqual(order_response[0].client_order_id, '1467403664')
        self.assertIsNone(order_response[0].exec_id)
        self.assertIsNone(order_response[0].exec_type)
        self.assertIsNone(order_response[0].message_type)
        self.assertIsNone(order_response[0].order_rejection_reason)
