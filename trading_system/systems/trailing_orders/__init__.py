from datetime import datetime

from trading_system import consts
from trading_system.systems.interfaces import ITradingSystem
from trading_system.systems.trailing_orders import commands


class TrailingOrders(ITradingSystem):
    """
    :type start_value: float
    :type stop_value: float
    :type order_placement_perc: float
    :type stop_loss_trigger: float
    :type next_operation: basestring
    :type is_tracking: bool
    :type balance: trading_system.api.beans.Balance
    :type pending_orders; list[trading_system.api.beans.PlacedOrder]
    """
    next_operation = NotImplemented
    is_tracking = NotImplemented
    balance = NotImplemented
    pending_orders = []

    def __init__(self, client):
        """
        :type client: trading_system.api.interfaces.IClient
        """
        self.client = client
        print('---------------------------------------')
        print('-----  SETUP THE TRAILING ORDERS  -----')
        print('---------------------------------------')
        self.start_value = self._get_start_value()
        self.stop_value = self._get_stop_value()
        self.order_placement_perc = self._get_order_placement_percentage()
        self.stop_loss_trigger = self._get_stop_loss_trigger()
        self.next_operation = self._get_next_operation()
        self.is_tracking = False
        print('System started with the following values:')
        print('    - Start value: {}'.format(self.start_value))
        print('    - Stop value: {}'.format(self.stop_value))
        print('    - Order Placement %: {}'.format(self.order_placement_perc))
        print('    - Stop Loss %: {}'.format(self.stop_loss_trigger))
        print('    - Next Operation: {}'.format(self.next_operation))
        print('    - Buy Price: {}'.format(self.buy_price))
        print('    - Sell Price: {}'.format(self.sell_price))
        print('    - Stop Loss Price: {}'.format(self.stop_loss_price))
        print('')
        print('    - Gross Margin: {}'.format(((self.sell_price / self.buy_price) - 1) * 100))

    @staticmethod
    def _get_start_value():
        print('')
        print('')
        print('START BUY value is the lowest price to start tracking the quote to *** BUY *** bitcoins.')
        print('After reaching lowest value and the price raises a order_placement_perc, '
              'the buying order will be placed.')
        print('')
        return float(input('Insert the value to START BUY: '))

    @staticmethod
    def _get_stop_value():
        print('')
        print('')
        print('START SELL value is the lowest price to start tracking the quote to *** SELL *** bitcoins.')
        print('After reaching highest value and the price falls an order_placement_perc, '
              'the selling order will be placed.')
        print('')
        return float(input('Insert the value to START SELL: '))

    @staticmethod
    def _get_order_placement_percentage():
        print('')
        print('')
        return float(input('Insert the order_placement_perc of gain/loss to place the order: '))

    @staticmethod
    def _get_stop_loss_trigger():
        print('')
        print('')
        print('If price continues to fall after the buy operation, it must be a good idea to put a STOP LOSS order '
              'to avoid loss more money.')
        print('When the price reach this limit, a selling order will be placed')
        print('Left it empty to skip stop loss setup')
        print('')
        return float(input('Insert the percentage to place the stop loss order: '))

    @staticmethod
    def _get_next_operation():
        print('')
        print('')
        print('Please, indicate what should be the first operation to track. 1 = BUY / 2 = SELL')
        print('')
        return input('Insert the first operation side: ')

    @property
    def buy_price(self):
        buy_price = self.start_value * ((100 + self.order_placement_perc) / 100)
        return self._get_rounded_value(buy_price)

    @property
    def sell_price(self):
        sell_price = self.stop_value * ((100.0 - self.order_placement_perc) / 100)
        return self._get_rounded_value(sell_price)

    @property
    def stop_loss_price(self):
        stop_loss_price = self.start_value * ((100.0 - self.stop_loss_trigger) / 100)
        return self._get_rounded_value(stop_loss_price)

    def run(self):
        self.pending_orders = self.client.orders.get_pending_orders(0, 2)
        self.balance = self.client.account.get_balance()
        current_ticker = self.client.market.get_ticker()
        command = self._get_command()
        command(self).execute(current_ticker.last_value)

        self.update_start_stop_values_if_necessary(current_ticker.last_value)

    def _get_command(self):
        if self.pending_orders[0] is not None:
            return commands.EvaluatePendingOrdersCommand

        return {
            consts.OrderSide.BUY: commands.BuyBitcoinsCommand,
            consts.OrderSide.SELL: commands.SellBitcoinsCommand,
        }[self.next_operation]

    def update_start_stop_values_if_necessary(self, last_quote):
        if self.start_value <= last_quote <= self.stop_value:
            return

        reference = self.start_value if last_quote < self.start_value else self.stop_value
        self.start_value = self._get_rounded_value(self.start_value * (last_quote / reference))
        self.stop_value = self._get_rounded_value(self.stop_value * (last_quote / reference))

    @staticmethod
    def _get_rounded_value(value):
        return round(value, 2)

    @staticmethod
    def log_info(text):
        curr = datetime.now()
        print('{time} - {text}'.format(time=curr.strftime('%Y-%m-%d %H:%M:%S'), text=text))
