from unittest import TestCase

import mock

from trading_system import consts
from trading_system.api import beans
from trading_system.api.markets import BlinkTradeMarketApi


class BlinkTradeOrdersApiTestCase(TestCase):
    def setUp(self):
        self.client = mock.Mock()
        self.client.environment_type = consts.Environment.PRODUCTION
        self.client.environment_server = 'http://www.bitcoin_exchange.com'
        self.client.currency = consts.Currency.BRAZILIAN_REAIS
        self.client.broker = consts.Broker.FOXBIT
        self.client.key = 'my_key'
        self.client.secret_key = 'my_secret_key'

        self.market_api = BlinkTradeMarketApi(self.client)

    @mock.patch('trading_system.api.markets.BlinkTradeMarketApi._get_market_data', mock.Mock(return_value={
        'high': 2299.9,
        'vol': 305.59416915,
        'buy': 2279.8,
        'last': 2295.98,
        'low': 2202.76,
        'pair': 'BTCBRL',
        'sell': 2295.98,
        'vol_brl': 691963.42220648
    }))
    def test_it_get_ticker(self):
        ticker = self.market_api.get_ticker()
        self.assertIsInstance(ticker, beans.Ticker)

    @mock.patch('trading_system.api.markets.BlinkTradeMarketApi._get_market_data', mock.Mock(return_value={
        'pair': 'BTCBRL',
        'bids': [[2279.9, 0.04213685, 90800428], [2279.89, 0.17024064, 90844402], [2279.87, 1.36183334, 90800428]],
        'asks': [[2295.98, 0.24452091, 90840688], [2296.16, 1.2047416, 90803493], [2296.4, 2.0, 90840688]],
    }))
    def test_it_get_order_book(self):
        order_book = self.market_api.get_order_book()
        self.assertIsInstance(order_book, beans.OrderBook)

    @mock.patch('trading_system.api.markets.BlinkTradeMarketApi._get_market_data', mock.Mock(return_value=[
        {"tid": 390596, "date": 1467037014, "price": 2300.0, "amount": 0.02847873, "side": "sell"},
        {"tid": 390601, "date": 1467037288, "price": 2302.65, "amount": 1.998, "side": "sell"},
        {"tid": 390603, "date": 1467037349, "price": 2302.65, "amount": 0.91031505, "side": "sell"},
    ]))
    def test_it_get_trades(self):
        trade_list = self.market_api.get_trade_list()
        self.assertIsInstance(trade_list, list)
        self.assertIsInstance(trade_list[0], beans.Trade)
