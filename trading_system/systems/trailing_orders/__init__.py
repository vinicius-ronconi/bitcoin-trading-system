from datetime import datetime
from trading_system.api import consts
from trading_system.api.clients import BlinkTradeClient
from trading_system.systems.interfaces import ITradingSystem
from trading_system.systems.settings import *


class TrailingOrders(ITradingSystem):
    """
    :type next_operation: basestring
    :type is_tracking: bool
    :type balance: trading_system.api.beans.Balance
    :type pending_orders; list[trading_system.api.beans.PlacedOrder]
    """
    next_operation = NotImplemented
    is_tracking = NotImplemented
    balance = NotImplemented
    pending_orders = []

    def __init__(self):
        print '---------------------------------------'
        print '-----  SETUP THE TRAILING ORDERS  -----'
        print '---------------------------------------'
        self.start_value = self._get_start_value()
        self.stop_value = self._get_stop_value()
        self.order_placement_perc = self._get_order_placement_percentage()
        self.stop_loss_trigger = self._get_stop_loss_trigger()
        self.next_operation = self._get_next_operation()
        self.is_tracking = False

        self.client = BlinkTradeClient(
            consts.Environment.PRODUCTION,
            consts.Currency.BRAZILIAN_REAIS,
            consts.Broker.FOXBIT,
            BLINKTRADE_KEY, BLINKTRADE_SECRET,
        )

    @staticmethod
    def _get_start_value():
        print ''
        print ''
        print 'START BUY value is the lowest price to start tracking the quote to *** BUY *** bitcoins.'
        print 'After reaching lowest value and the price raises a order_placement_perc, ' \
              'the buying order will be placed.'
        print ''
        return raw_input('Insert the value to START BUY: ')

    @staticmethod
    def _get_stop_value():
        print ''
        print ''
        print 'START SELL value is the lowest price to start tracking the quote to *** SELL *** bitcoins.'
        print 'After reaching highest value and the price falls an order_placement_perc, ' \
              'the selling order will be placed.'
        print ''
        return raw_input('Insert the value to START SELL: ')

    @staticmethod
    def _get_order_placement_percentage():
        print ''
        print ''
        return raw_input('Insert the order_placement_perc of gain/loss to place the order: ')

    @staticmethod
    def _get_stop_loss_trigger():
        print ''
        print ''
        print 'If price continues to fall after the buy operation, it must be a good idea to put a STOP LOSS order ' \
              'to avoid loss more money.'
        print 'When the price reach this limit, a selling order will be placed'
        print 'Left it empty to skip stop loss setup'
        print ''
        return raw_input('Insert the order_placement_perc to place the stop loss order: ')

    @staticmethod
    def _get_next_operation():
        print ''
        print ''
        print 'Please, indicate what should be the first operation to track. 1 = BUY / 2 = SELL'
        print ''
        return raw_input('Insert the first operation side: ')

    @property
    def buy_price(self):
        buy_price = self.start_value * ((100 + self.order_placement_perc) / 100)
        return self._get_rounded_value(buy_price)

    @property
    def sell_price(self):
        sell_price = self.stop_value * ((100 - self.order_placement_perc) / 100)
        return self._get_rounded_value(sell_price)

    def run(self):
        self.pending_orders = self.client.orders.get_pending_orders(0, 2)
        self.balance = self.client.account.get_balance()
        current_ticker = self.client.market.get_ticker()
        evaluate_func = self._get_evaluation_type()
        evaluate_func(current_ticker.last_value)

    def _get_evaluation_type(self):
        if self.pending_orders:
            return self.evaluate_pending_orders

        return {
            consts.OrderSide.BUY: self.evaluate_buying_conditions,
            consts.OrderSide.SELL: self.evaluate_selling_conditions,
        }[self.next_operation]

    def evaluate_pending_orders(self, last_quote):
        # TODO Check if should cancel order
        # Cancel buying order if last_quote > order price * order_placement_perc
        # Cancel selling order if last_quote < order price * order_placement_perc
        pass

    def evaluate_buying_conditions(self, last_quote):
        evaluate_func = self._get_buy_operation_func()
        evaluate_func(last_quote)

    def _get_buy_operation_func(self):
        return {
            True: self.evaluate_last_quote_to_buy_bitcoins,
            False: self.evaluate_last_quote_to_start_buying_track,
        }[self.is_tracking]

    def evaluate_last_quote_to_buy_bitcoins(self, last_quote):
        if last_quote >= self.buy_price:
            quantity = self.client.get_satoshi_value(self.balance.currency/last_quote)
            self.log_info('BUYING {quantity} BITCOINS - price: {value}'.format(quantity=quantity, value=last_quote))
            self.client.orders.buy_bitcoins(consts.OrderType.LIMITED_ORDER, last_quote, quantity)
            self.next_operation = consts.OrderSide.SELL
            self.is_tracking = False

    @staticmethod
    def _get_rounded_value(value):
        return round(value, 2)

    def evaluate_last_quote_to_start_buying_track(self, last_quote):
        self.is_tracking = last_quote <= self.start_value
        if self.is_tracking:
            self.log_info('Tracking values to place a buy order')

    def evaluate_selling_conditions(self, last_quote):
        pass

    @staticmethod
    def log_info(text):
        curr = datetime.now()
        print '{time} - {text}'.format(time=curr.strftime('%Y-%m-%d %H:%M:%S'), text=text)


if __name__ == '__main__':
    system = TrailingOrders()
    system.run()
