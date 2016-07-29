from unittest import TestCase

import mock

from trading_system import consts
from trading_system.api import beans
from trading_system.api.bitfinex.clients import BitfinexClient
from trading_system.api.bitfinex.markets import BitfinexMarketApi


class BitfinexMarketApiTestCase(TestCase):
    market_api = NotImplemented

    def setUp(self):
        client = BitfinexClient(consts.Environment.PRODUCTION, consts.Symbol.BTCUSD, 'my_key', 'my_secret')
        self.market_api = BitfinexMarketApi(client)

    def test_it_get_ticker(self):
        self.market_api.client.api.ticker = mock.Mock(return_value={
            'mid': '245.0',
            'bid': '245.0',
            'timestamp': '1444253422',
            'last_price': '250.0',
            'ask': '246.0',
        })
        self.market_api.client.api.today = mock.Mock(return_value={
            'low': '240.0', 'high': '250.0', 'volume': '1000.0'
        })
        ticker = self.market_api.get_ticker()
        self.assertIsInstance(ticker, beans.Ticker)
        self.assertEqual(ticker.highest_value, 250.0)
        self.assertEqual(ticker.volume_btc, 1000.0)
        self.assertEqual(ticker.best_buy_order, 245.0)
        self.assertEqual(ticker.last_value, 250.0)
        self.assertEqual(ticker.lowest_value, 240.0)
        self.assertEqual(ticker.best_sell_order, 246.0)
        self.assertEqual(ticker.volume_currency, 250000.0)

    def test_it_get_order_book(self):
        self.market_api.client.api.order_book = mock.Mock(return_value={
            'bids': [{'price': '500.0', 'amount': '1.5', 'timestamp': '1395557729.0'}],
            'asks': [{'price': '600.0', 'amount': '2.5', 'timestamp': '1395557711.0'}]
        })

        order_book = self.market_api.get_order_book()
        self.assertIsInstance(order_book, beans.OrderBook)
        self.assertIsInstance(order_book.bids, list)
        self.assertIsInstance(order_book.bids[0], beans.OrderInBook)
        self.assertEqual(order_book.bids[0].price, 500.0)
        self.assertEqual(order_book.bids[0].amount, 1.5)
        self.assertIsNone(order_book.bids[0].user_id)
        self.assertIsInstance(order_book.asks, list)
        self.assertIsInstance(order_book.asks[0], beans.OrderInBook)
        self.assertEqual(order_book.asks[0].price, 600.0)
        self.assertEqual(order_book.asks[0].amount, 2.5)
        self.assertIsNone(order_book.asks[0].user_id)

    def test_it_get_trades(self):
        self.market_api.client.api._get = mock.Mock(return_value=[{
            'timestamp': 1444266681,
            'tid': 1000,
            'price': '500.0',
            'amount': '1.5',
            'exchange': 'bitfinex',
            'type': 'sell'
        }])
        trade_list = self.market_api.get_trade_list()
        self.assertIsInstance(trade_list, list)
        self.assertIsInstance(trade_list[0], beans.Trade)
        self.assertEqual(trade_list[0].transaction_id, 1000)
        self.assertEqual(trade_list[0].date, 1444266681)
        self.assertEqual(trade_list[0].price, 500.0)
        self.assertEqual(trade_list[0].amount, 1.5)
        self.assertEqual(trade_list[0].side, 'sell')
