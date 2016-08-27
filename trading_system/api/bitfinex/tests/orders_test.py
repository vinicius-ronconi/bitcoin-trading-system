from unittest import TestCase

import mock

from trading_system import consts
from trading_system.api import beans
from trading_system.api.bitfinex.clients import BitfinexClient
from trading_system.api.bitfinex.orders import BitfinexOrdersApi


class BitfinexOrdersApiTestCase(TestCase):
    orders_api = NotImplemented

    def setUp(self):
        client = BitfinexClient(consts.Environment.PRODUCTION, consts.Symbol.BTCUSD, 'my_key', 'my_secret')
        self.orders_api = BitfinexOrdersApi(client)

    def test_it_places_a_limited_buy_order(self):
        self.orders_api.client.auth_api.place_order = mock.Mock(return_value={
            'id': 448364249,
            'symbol': 'btcusd',
            'exchange': 'bitfinex',
            'price': '2175.0',
            'avg_execution_price': '0.0',
            'side': 'buy',
            'type': 'exchange limit',
            'timestamp': '1444272165.252370982',
            'is_live': True,
            'is_cancelled': False,
            'is_hidden': False,
            'was_forced': False,
            'original_amount': '0.0313',
            'remaining_amount': '0.0313',
            'executed_amount': '0.0',
            'order_id': 448364249,
        })
        order_response = self.orders_api.buy_bitcoins_with_limited_order(price=2175, quantity=0.0313)
        self.assertIsInstance(order_response, beans.PlacedOrder)
        self.assertEqual(order_response.order_id, '448364249')
        self.assertEqual(order_response.exec_id, '448364249')
        self.assertEqual(order_response.exec_type, 'exchange limit')
        self.assertEqual(order_response.order_status, self.orders_api.ORDER_STATUS_NEW)
        self.assertEqual(order_response.price, 2175.0)
        self.assertEqual(order_response.symbol, consts.Symbol.BTCUSD)
        self.assertEqual(order_response.amount, 0.0313)
        self.assertEqual(order_response.side, 'buy')
        self.assertEqual(order_response.client_order_id, '448364249')
        self.assertIsNone(order_response.message_type)
        self.assertIsNone(order_response.order_rejection_reason)

    def test_it_places_a_market_buy_order(self):
        self.orders_api.client.auth_api.place_order = mock.Mock(return_value={
            'order_id': 1026178983,
            'id': 1026178983,
            'avg_execution_price': '0.0',
            'is_cancelled': False,
            'remaining_amount': '0.0313',
            'exchange': 'bitfinex',
            'symbol': 'btcusd',
            'was_forced': False,
            'is_hidden': False,
            'type': 'exchange market',
            'oco_order': None,
            'price': '0.01',
            'executed_amount': '0.0',
            'timestamp': '1471637931.800969379',
            'is_live': True,
            'side': 'buy',
            'original_amount': '0.0313'
        })
        order_response = self.orders_api.buy_bitcoins_with_market_order(quantity=0.0313)
        self.assertIsInstance(order_response, beans.PlacedOrder)
        self.assertEqual(order_response.order_id, '1026178983')
        self.assertEqual(order_response.exec_id, '1026178983')
        self.assertEqual(order_response.exec_type, 'exchange market')
        self.assertEqual(order_response.order_status, self.orders_api.ORDER_STATUS_NEW)
        self.assertEqual(order_response.symbol, consts.Symbol.BTCUSD)
        self.assertEqual(order_response.amount, 0.0313)
        self.assertEqual(order_response.side, 'buy')
        self.assertEqual(order_response.client_order_id, '1026178983')
        self.assertIsNone(order_response.message_type)
        self.assertIsNone(order_response.order_rejection_reason)

    def test_it_places_a_limited_sell_order(self):
        self.orders_api.client.auth_api.place_order = mock.Mock(return_value={
            'id': 448364249,
            'symbol': 'btcusd',
            'exchange': 'bitfinex',
            'price': '2175.0',
            'avg_execution_price': '0.0',
            'side': 'sell',
            'type': 'exchange limit',
            'timestamp': '1444272165.252370982',
            'is_live': True,
            'is_cancelled': False,
            'is_hidden': False,
            'was_forced': False,
            'original_amount': '0.0313',
            'remaining_amount': '0.0313',
            'executed_amount': '0.0',
            'order_id': 448364249,
        })
        order_response = self.orders_api.sell_bitcoins_with_limited_order(price=2175, quantity=0.0313)
        self.assertIsInstance(order_response, beans.PlacedOrder)
        self.assertEqual(order_response.order_id, '448364249')
        self.assertEqual(order_response.exec_id, '448364249')
        self.assertEqual(order_response.exec_type, 'exchange limit')
        self.assertEqual(order_response.order_status, self.orders_api.ORDER_STATUS_NEW)
        self.assertEqual(order_response.price, 2175.0)
        self.assertEqual(order_response.symbol, consts.Symbol.BTCUSD)
        self.assertEqual(order_response.amount, 0.0313)
        self.assertEqual(order_response.side, 'sell')
        self.assertEqual(order_response.client_order_id, '448364249')
        self.assertIsNone(order_response.message_type)
        self.assertIsNone(order_response.order_rejection_reason)

    def test_it_places_a_market_sell_order(self):
        self.orders_api.client.auth_api.place_order = mock.Mock(return_value={
            'order_id': 1026166073,
            'executed_amount': '0.0',
            'avg_execution_price': '0.0',
            'type': 'exchange market',
            'is_hidden': False,
            'timestamp': '1471637737.143232426',
            'price': '600.0',
            'side': 'sell',
            'exchange': 'bitfinex',
            'symbol': 'btcusd',
            'is_live': True,
            'id': 1026166073,
            'is_cancelled': False,
            'oco_order': None,
            'original_amount': '0.0313',
            'remaining_amount': '0.0313',
            'was_forced': False
        })
        order_response = self.orders_api.sell_bitcoins_with_market_order(quantity=0.0313)
        self.assertIsInstance(order_response, beans.PlacedOrder)
        self.assertEqual(order_response.order_id, '1026166073')
        self.assertEqual(order_response.exec_id, '1026166073')
        self.assertEqual(order_response.exec_type, 'exchange market')
        self.assertEqual(order_response.order_status, self.orders_api.ORDER_STATUS_NEW)
        self.assertEqual(order_response.symbol, consts.Symbol.BTCUSD)
        self.assertEqual(order_response.amount, 0.0313)
        self.assertEqual(order_response.side, 'sell')
        self.assertEqual(order_response.client_order_id, '1026166073')
        self.assertIsNone(order_response.message_type)
        self.assertIsNone(order_response.order_rejection_reason)

    def test_it_cancels_an_order(self):
        self.orders_api.client.auth_api.delete_order = mock.Mock(return_value={
            'id': 446915287,
            'symbol': 'btcusd',
            'exchange': None,
            'price': '2175.0',
            'avg_execution_price': '0.0',
            'side': 'sell',
            'type': 'exchange limit',
            'timestamp': '1444141982.0',
            'is_live': False,
            'is_cancelled': True,
            'is_hidden': False,
            'was_forced': False,
            'original_amount': '0.0313',
            'remaining_amount': '0.0313',
            'executed_amount': '0.0',
        })
        order_response = self.orders_api.cancel_order(1)
        self.assertIsInstance(order_response, beans.PlacedOrder)
        self.assertEqual(order_response.exec_id, '446915287')
        self.assertEqual(order_response.exec_type, 'exchange limit')
        self.assertEqual(order_response.order_status, self.orders_api.ORDER_STATUS_CANCELLED)
        self.assertEqual(order_response.price, 2175.0)
        self.assertEqual(order_response.symbol, consts.Symbol.BTCUSD)
        self.assertEqual(order_response.amount, 0.0313)
        self.assertEqual(order_response.side, 'sell')
        self.assertIsNone(order_response.order_id)
        self.assertIsNone(order_response.message_type)
        self.assertIsNone(order_response.order_rejection_reason)
        self.assertIsNone(order_response.client_order_id)

    def test_it_gets_pending_orders(self):
        self.orders_api.client.auth_api.active_orders = mock.Mock(return_value=[{
            'id': 448411365,
            'symbol': 'btcusd',
            'exchange': 'bitfinex',
            'price': '2175.0',
            'avg_execution_price': '0.0',
            'side': 'buy',
            'type': 'exchange limit',
            'timestamp': '1444276597.0',
            'is_live': True,
            'is_cancelled': False,
            'is_hidden': False,
            'was_forced': False,
            'original_amount': '0.0313',
            'remaining_amount': '0.0313',
            'executed_amount': '0.0',
        }])
        orders = self.orders_api.get_pending_orders(page=0, page_size=10)
        self.assertIsInstance(orders, list)
        order_response = orders[0]
        self.assertIsInstance(order_response, beans.PlacedOrder)
        self.assertEqual(order_response.exec_id, '448411365')
        self.assertEqual(order_response.exec_type, 'exchange limit')
        self.assertEqual(order_response.order_status, self.orders_api.ORDER_STATUS_NEW)
        self.assertEqual(order_response.price, 2175.0)
        self.assertEqual(order_response.symbol, consts.Symbol.BTCUSD)
        self.assertEqual(order_response.amount, 0.0313)
        self.assertEqual(order_response.side, 'buy')
        self.assertIsNone(order_response.order_id)
        self.assertIsNone(order_response.message_type)
        self.assertIsNone(order_response.order_rejection_reason)
        self.assertIsNone(order_response.client_order_id)
