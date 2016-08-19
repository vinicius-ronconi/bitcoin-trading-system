from time import time

from trading_system.api import beans
from trading_system.api.interfaces import IMarketApi


class BitfinexMarketApi(IMarketApi):
    def __init__(self, client):
        """
        :type client: trading_system.api.bitfinex.clients.BitfinexClient
        """
        self.client = client

    def get_ticker(self):
        ticker = self.client.open_api.ticker(self.client.symbol)
        today = self.client.open_api.today(self.client.symbol)
        return beans.Ticker(
            currency_pair=self.client.symbol,
            last_value=float(ticker.get('last_price')),
            highest_value=float(today.get('high')),
            lowest_value=float(today.get('low')),
            best_sell_order=float(ticker.get('ask')),
            best_buy_order=float(ticker.get('bid')),
            volume_btc=float(today.get('volume')),
            volume_currency=float(today.get('volume', 0)) * float(ticker.get('last_price', 0)),
        )

    def get_order_book(self):
        response = self.client.open_api.order_book(self.client.symbol, parameters={'limit_bids': 2, 'limit_asks': 2})
        return beans.OrderBook(
            currency_pair=self.client.symbol,
            bids=[
                beans.OrderInBook(
                    price=float(bid['price']), amount=float(bid['amount']), user_id=None
                ) for bid in response.get('bids')
            ],
            asks=[
                beans.OrderInBook(
                    price=float(ask['price']), amount=float(ask['amount']), user_id=None
                ) for ask in response.get('asks')
            ],
        )

    def get_trade_list(self, offset=3600):
        trades = self.client.open_api._get(self.client.open_api.url_for(
            'trades/%s', path_arg=self.client.symbol, parameters={'timestamp': int(time()) - offset}
        ))
        return [beans.Trade(
            transaction_id=int(trade.get('tid')),
            date=int(trade.get('timestamp')),
            price=float(trade.get('price')),
            amount=float(trade.get('amount')),
            side=trade.get('type')
        ) for trade in trades]
