from unittest import TestCase

import mock

from trading_system import consts
from trading_system.api import beans
from trading_system.api import exceptions
from trading_system.api.blinktrade.clients import BlinkTradeClient
from trading_system.api.blinktrade.orders import BlinkTradeOrdersApi


class BlinkTradeOrdersApiTestCase(TestCase):
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

    def test_it_places_a_buy_order(self):
        self.orders_api.client.send_request = mock.Mock(return_value={
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
                    u'4': {u'BRL_locked': 5500000000},
                    u'ClientID': 90856083
                }
            ]

        })
        order_response = self.orders_api.buy_bitcoins(consts.OrderType.LIMITED_ORDER, price=2175, quantity=0.0313)
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
        self.assertEqual(order_response[1].currency_locked, 55.0)

    def test_it_does_not_accept_an_order_with_too_small_value(self):
        self.orders_api.client.send_request = mock.Mock(return_value={
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
        })
        self.assertRaises(
            exceptions.OrderRejectedException,
            self.orders_api.buy_bitcoins,
            order_type=consts.OrderType.LIMITED_ORDER,
            price=0.01,
            quantity=0.00000001,
        )

    def test_it_places_a_sell_order(self):
        self.orders_api.client.send_request = mock.Mock(return_value={
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
                    u'4': {u'BRL_locked': 5500000000},
                    u'ClientID': 90856083
                }
            ]
        })
        order_response = self.orders_api.sell_bitcoins(consts.OrderType.LIMITED_ORDER, price=2175, quantity=0.0313)
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
        self.assertEqual(order_response[1].currency_locked, 55.0)

    def test_it_cancels_an_order(self):
        self.orders_api.client.send_request = mock.Mock(return_value={
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
        })
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
        self.assertEqual(order_response[1].currency_locked, 0.0)

    def test_it_gets_pending_orders(self):
        self.orders_api.client.send_request = mock.Mock(return_value={
            u'Status': 200,
            u'Description': u'OK',
            u'Responses': [
                {
                    u'OrdListGrp': [
                        [
                            u'2961106',
                            1459144231834,
                            0,
                            u'0',
                            3220000,
                            0,
                            0,
                            u'BTCBRL',
                            u'1',
                            u'2',
                            3220000,
                            225800000000,
                            u'2016-07-06 13:44:53',
                            0,
                            u'1'
                        ]
                    ],
                    u'PageSize': 20,
                    u'OrdersReqID': 1467837196,
                    u'MsgType': u'U5',
                    u'Page': 0,
                    u'Columns': [
                        u'ClOrdID',
                        u'OrderID',
                        u'CumQty',
                        u'OrdStatus',
                        u'LeavesQty',
                        u'CxlQty',
                        u'AvgPx',
                        u'Symbol',
                        u'Side',
                        u'OrdType',
                        u'OrderQty',
                        u'Price',
                        u'OrderDate',
                        u'Volume',
                        u'TimeInForce',
                    ]
                }
            ]
        })
        order_response = self.orders_api.get_pending_orders(page=0, page_size=100)
        self.assertIsInstance(order_response, list)
        self.assertIsInstance(order_response[0], beans.PlacedOrder)
        self.assertEqual(order_response[0].order_id, '1459144231834')
        self.assertEqual(order_response[0].order_status, '0')
        self.assertEqual(order_response[0].price, 2258.0)
        self.assertEqual(order_response[0].symbol, 'BTCBRL')
        self.assertEqual(order_response[0].amount, 0.0322)
        self.assertEqual(order_response[0].side, '1')
        self.assertEqual(order_response[0].client_order_id, '2961106')
        self.assertIsNone(order_response[0].exec_id)
        self.assertIsNone(order_response[0].exec_type)
        self.assertIsNone(order_response[0].message_type)
        self.assertIsNone(order_response[0].order_rejection_reason)

    def test_it_gets_executed_orders(self):
        self.orders_api.client.send_request = mock.Mock(return_value={
            u'Status': 200,
            u'Description': u'OK',
            u'Responses': [
                {
                    u'OrdListGrp': [
                        [
                            u'2961106',
                            1459144231834,
                            0,
                            u'0',
                            3220499,
                            0,
                            0,
                            u'BTCBRL',
                            u'1',
                            u'2',
                            3220000,
                            225800000000,
                            u'2016-07-06 13:44:53',
                            0,
                            u'1'
                        ]
                    ],
                    u'PageSize': 20,
                    u'OrdersReqID': 1467837196,
                    u'MsgType': u'U5',
                    u'Page': 0,
                    u'Columns': [
                        u'ClOrdID',
                        u'OrderID',
                        u'CumQty',
                        u'OrdStatus',
                        u'LeavesQty',
                        u'CxlQty',
                        u'AvgPx',
                        u'Symbol',
                        u'Side',
                        u'OrdType',
                        u'OrderQty',
                        u'Price',
                        u'OrderDate',
                        u'Volume',
                        u'TimeInForce'
                    ]
                }
            ]
        })
        order_response = self.orders_api.get_executed_orders(page=0, page_size=100)
        self.assertIsInstance(order_response, list)
        self.assertIsInstance(order_response[0], beans.PlacedOrder)
        self.assertEqual(order_response[0].order_id, '1459144231834')
        self.assertEqual(order_response[0].order_status, '0')
        self.assertEqual(order_response[0].price, 2258.0)
        self.assertEqual(order_response[0].symbol, 'BTCBRL')
        self.assertEqual(order_response[0].amount, 0.0322)
        self.assertEqual(order_response[0].side, '1')
        self.assertEqual(order_response[0].client_order_id, '2961106')
        self.assertIsNone(order_response[0].exec_id)
        self.assertIsNone(order_response[0].exec_type)
        self.assertIsNone(order_response[0].message_type)
        self.assertIsNone(order_response[0].order_rejection_reason)
