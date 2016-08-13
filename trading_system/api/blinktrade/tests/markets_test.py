from unittest import TestCase

import mock

from trading_system import consts
from trading_system.api import beans
from trading_system.api.blinktrade.clients import BlinkTradeClient
from trading_system.api.blinktrade.markets import BlinkTradeMarketApi


class MarketTestCase(TestCase):
    def setUp(self):
        client = BlinkTradeClient(
            consts.Environment.PRODUCTION,
            consts.Currency.BRAZILIAN_REAIS,
            consts.Broker.FOXBIT,
            'my_key',
            'my_secret',
        )
        self.market_api = BlinkTradeMarketApi(client)

    @mock.patch('blinktrade.clients.OpenClient.get_ticker', mock.Mock(return_value={
        'high': 2299.9,
        'vol': 305.5,
        'buy': 2279.8,
        'last': 2295.98,
        'low': 2202.76,
        'pair': 'BTCBRL',
        'sell': 2295.98,
        'vol_brl': 691963.42
    }))
    def test_it_get_ticker(self):
        ticker = self.market_api.get_ticker()
        self.assertIsInstance(ticker, beans.Ticker)
        self.assertEqual(ticker.highest_value, 2299.9)
        self.assertEqual(ticker.volume_btc, 305.5)
        self.assertEqual(ticker.best_buy_order, 2279.8)
        self.assertEqual(ticker.last_value, 2295.98)
        self.assertEqual(ticker.lowest_value, 2202.76)
        self.assertEqual(ticker.best_sell_order, 2295.98)
        self.assertEqual(ticker.volume_currency, 691963.42)

    @mock.patch('blinktrade.clients.OpenClient.get_order_book', mock.Mock(return_value={
        'pair': 'BTCBRL',
        'bids': [[2279.9, 0.0421, 1000], ],
        'asks': [[2295.9, 0.2445, 2000], ],
    }))
    def test_it_get_order_book(self):
        order_book = self.market_api.get_order_book()
        self.assertIsInstance(order_book, beans.OrderBook)
        self.assertIsInstance(order_book.bids, list)
        self.assertIsInstance(order_book.bids[0], beans.OrderInBook)
        self.assertEqual(order_book.bids[0].price, 2279.9)
        self.assertEqual(order_book.bids[0].amount, 0.0421)
        self.assertEqual(order_book.bids[0].user_id, 1000)
        self.assertIsInstance(order_book.asks, list)
        self.assertIsInstance(order_book.asks[0], beans.OrderInBook)
        self.assertEqual(order_book.asks[0].price, 2295.9)
        self.assertEqual(order_book.asks[0].amount, 0.2445)
        self.assertEqual(order_book.asks[0].user_id, 2000)

    @mock.patch('blinktrade.clients.OpenClient.get_trade_list', mock.Mock(return_value=[
        {'tid': 1000, 'date': 1467037014, 'price': 2300.0, 'amount': 0.02, 'side': 'sell'},
    ]))
    def test_it_get_trades(self):
        trade_list = self.market_api.get_trade_list()
        self.assertIsInstance(trade_list, list)
        self.assertIsInstance(trade_list[0], beans.Trade)
        self.assertEqual(trade_list[0].transaction_id, 1000)
        self.assertEqual(trade_list[0].date, 1467037014)
        self.assertEqual(trade_list[0].price, 2300.0)
        self.assertEqual(trade_list[0].amount, 0.02)
        self.assertEqual(trade_list[0].side, 'sell')
