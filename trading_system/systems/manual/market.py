import operator
from trading_system.api.clients import BlinkTradeClient
from trading_system.api import consts
from trading_system.systems.settings import *


class ManualTradingSystem(object):
    def __init__(self):
        self.client = BlinkTradeClient(
            consts.Environment.PRODUCTION,
            consts.Currency.BRAZILIAN_REAIS,
            consts.Broker.FOXBIT,
            BLINKTRADE_KEY, BLINKTRADE_SECRET,
        )

    def get_order_book(self):
        return self.client.market.get_order_book()

    def show_orders_grouped_by_user(self, valid_percentage):
        order_book = self.get_order_book()
        ticker = self.client.market.get_ticker()
        valid_bid_price = ticker.last_value * (100.0 - valid_percentage)/100
        valid_ask_price = ticker.last_value * (100.0 + valid_percentage)/100
        print 'last value = {}'.format(ticker.last_value)
        print 'valid bid = {}'.format(valid_bid_price)
        print 'valid ask = {}'.format(valid_ask_price)

        valid_bids = [bid for bid in order_book.bids if bid.price >= valid_bid_price]
        grouped_bids = self._group_list_by_user(valid_bids)
        valid_asks = [ask for ask in order_book.asks if ask.price <= valid_ask_price]
        grouped_asks = self._group_list_by_user(valid_asks)
        print '{quantity} bidders - Amount: {amount}'.format(
            quantity=len(grouped_bids), amount=self._get_total_amount(grouped_bids)
        )
        print '{quantity} askers - Amount: {amount}'.format(
            quantity=len(grouped_asks), amount=self._get_total_amount(grouped_asks)
        )
        print grouped_bids
        print grouped_asks

    @staticmethod
    def _group_list_by_user(order_list):
        grouped_dict = {}
        for order in order_list:
            grouped_dict[order.user_id] = grouped_dict.get(order.user_id, 0) + order.amount
        return sorted(grouped_dict.items(), key=operator.itemgetter(1), reverse=True)

    @staticmethod
    def _get_total_amount(tuples_list):
        return sum([item[1] for item in tuples_list])

if __name__ == '__main__':
    system = ManualTradingSystem()
    system.show_orders_grouped_by_user(valid_percentage=5)
