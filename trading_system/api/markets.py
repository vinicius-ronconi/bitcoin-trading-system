import time
import requests

from trading_system.api import beans
from trading_system.api import consts
from trading_system.api.interfaces import IMarketApi


class BlinkTradeMarketApi(IMarketApi):
    def __init__(self, client):
        """
        :type client: trading_system.api.clients.BlinkTradeClient
        """
        self.client = client

    def get_ticker(self):
        response = self._get_market_data(consts.MarketInformation.TICKER)
        return beans.Ticker(
            currency_pair=str(response.get('pair')),
            last_value=float(response.get('last')),
            highest_value=float(response.get('high')),
            lowest_value=float(response.get('low')),
            best_sell_order=float(response.get('sell')),
            best_buy_order=float(response.get('buy')),
            volume_btc=float(response.get('vol')),
            volume_currency=float(response.get('vol_{currency}'.format(currency=self.client.currency.lower()))),
        )

    def get_order_book(self):
        response = self._get_market_data(consts.MarketInformation.ORDER_BOOK)
        return beans.OrderBook(
            currency_pair=str(response.get('pair')),
            bids=[beans.OrderInBook(price=bid[0], amount=bid[1], user_id=bid[2]) for bid in response.get('bids')],
            asks=[beans.OrderInBook(price=bid[0], amount=bid[1], user_id=bid[2]) for bid in response.get('asks')],
        )

    def get_trade_list(self, offset=3600):
        response = self._get_market_data(
            consts.MarketInformation.TRADES, params='?since={offset}'.format(offset=int(time.time()) - offset),
        )
        return [beans.Trade(
            transaction_id=long(item.get('tid')),
            date=long(item.get('date')),
            price=float(item.get('price')),
            amount=float(item.get('amount')),
            side=str(item.get('side')),
        ) for item in response]

    def _get_market_data(self, requested_info, params=''):
        url = '{domain}/api/{version}/{currency}/{type}{params}'.format(
            domain=self.client.environment_server,
            version=self.client.API_VERSION,
            currency=self.client.currency,
            type=requested_info,
            params=params,
        )
        return requests.get(url).json()
