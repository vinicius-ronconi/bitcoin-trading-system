from trading_system.api import beans
from trading_system.api.interfaces import IMarketApi


class BlinkTradeMarketApi(IMarketApi):
    def __init__(self, client):
        """
        :type client: trading_system.api.blinktrade.clients.BlinkTradeClient
        """
        self.client = client

    def get_ticker(self):
        response = self.client.open_api.get_ticker()
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
        response = self.client.open_api.get_order_book()
        return beans.OrderBook(
            currency_pair=str(response.get('pair')),
            bids=[beans.OrderInBook(price=bid[0], amount=bid[1], user_id=bid[2]) for bid in response.get('bids')],
            asks=[beans.OrderInBook(price=bid[0], amount=bid[1], user_id=bid[2]) for bid in response.get('asks')],
        )

    def get_trade_list(self, since_ts=0):
        response = self.client.open_api.get_trade_list(since_ts)
        return [beans.Trade(
            transaction_id=int(item.get('tid')),
            date=int(item.get('date')),
            price=float(item.get('price')),
            amount=float(item.get('amount')),
            side=str(item.get('side')),
        ) for item in response]
