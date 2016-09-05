from datetime import datetime

from trading_system import consts
from trading_system.systems.interfaces import ITradingSystem
from trading_system.systems.trailing_orders import beans, commands, utils
from trading_system.utils import get_rounded_decimal_value


class TrailingOrders(ITradingSystem):
    """
    :type setup: trading_system.systems.trailing_orders.beans.TrailingOrderSetup
    :type is_tracking: bool
    :type balance: trading_system.api.beans.Balance
    :type pending_orders: list[trading_system.api.beans.PlacedOrder]
    """
    setup = NotImplemented
    is_tracking = NotImplemented
    balance = NotImplemented
    pending_orders = []

    def __init__(self, client):
        """
        :type client: trading_system.api.interfaces.IClient
        """
        self.client = client
        self.setup = SystemBootstrap().get_initial_setup()
        self.is_tracking = False

        print('System started with the following values:')
        print('    - Next Operation: {}'.format(self.setup.next_operation))
        print('    - Start value: {}'.format(self.setup.start_value))
        print('    - Buy Price: {}'.format(self.buy_price))
        print('    - Sell Price: {}'.format(self.sell_price))
        print('    - Stop value: {}'.format(self.setup.stop_value))
        print('    - Reversal %: {}'.format(self.setup.reversal))
        print('')
        print('    - Stop Loss %: {}'.format(self.setup.stop_loss))
        print('    - Stop Loss Price: {}'.format(self.stop_loss_price))
        print('')
        print('    - Gross Margin: {}'.format(
            get_rounded_decimal_value(((self.sell_price / self.buy_price) - 1) * 100))
        )

    @property
    def buy_price(self):
        return utils.get_buy_price(self.setup.start_value, self.setup.reversal)

    @property
    def sell_price(self):
        return utils.get_sell_price(self.setup.stop_value, self.setup.reversal)

    @property
    def stop_loss_price(self):
        return utils.get_stop_loss_price(self.setup.start_value, self.setup.stop_loss)

    def run(self):
        self.pending_orders = self._get_pending_orders()
        self.balance = self._get_balance()
        current_ticker = self._get_current_ticker()
        command = self._get_command()
        command(self).execute(current_ticker.last_value)

        self.update_start_stop_values_if_necessary(current_ticker.last_value)

    def _get_pending_orders(self):
        return self.client.orders.get_pending_orders(page=0, page_size=5)

    def _get_balance(self):
        return self.client.account.get_balance()

    def _get_current_ticker(self):
        return self.client.market.get_ticker()

    def _get_command(self):
        if self.pending_orders:
            return commands.EvaluatePendingOrdersCommand

        return {
            consts.OrderSide.BUY: commands.BuyBitcoinsCommand,
            consts.OrderSide.SELL: commands.SellBitcoinsCommand,
        }[self.setup.next_operation]

    def update_start_stop_values_if_necessary(self, last_quote):
        if self.setup.next_operation == consts.OrderSide.BUY and last_quote >= self.setup.start_value:
            return
        if self.setup.next_operation == consts.OrderSide.SELL and last_quote <= self.setup.stop_value:
            return

        reference = self.setup.start_value if last_quote < self.setup.start_value else self.setup.stop_value
        self.setup = beans.TrailingOrderSetup(
            next_operation=self.setup.next_operation,
            start_value=get_rounded_decimal_value(self.setup.start_value * (last_quote / reference)),
            stop_value=get_rounded_decimal_value(self.setup.stop_value * (last_quote / reference)),
            reversal=self.setup.reversal,
            stop_loss=self.setup.stop_loss,
            operational_cost=self.setup.operational_cost,
            profit=self.setup.profit,
        )
        self.log_info('Adjusting START and STOP values after last_quote = {}.'.format(last_quote))
        self.log_info('    . New start value is {}.'.format(self.setup.start_value))
        self.log_info('    . New stop value is {}.'.format(self.setup.stop_value))
        self.log_info('    . New buy price is {}.'.format(self.buy_price))
        self.log_info('    . New sell price is {}.'.format(self.sell_price))
        self.log_info('    . New stop loss price is {}.'.format(self.stop_loss_price))

    @staticmethod
    def log_info(text):
        curr = datetime.now()
        print('{time} - {text}'.format(time=curr.strftime('%Y-%m-%d %H:%M:%S'), text=text))

    def set_next_operation(self, next_operation):
        self.setup = beans.TrailingOrderSetup(
            next_operation=next_operation,
            start_value=self.setup.start_value,
            stop_value=self.setup.stop_value,
            reversal=self.setup.reversal,
            stop_loss=self.setup.stop_loss,
            operational_cost=self.setup.operational_cost,
            profit=self.setup.profit,
        )


class SystemBootstrap(object):
    # TODO: Create an interface and a Fake implementation to the tests
    def get_initial_setup(self):
        print('---------------------------------------')
        print('-----  SETUP THE TRAILING ORDERS  -----')
        print('---------------------------------------')
        next_operation = self._get_next_operation()
        setup_func = {
            consts.OrderSide.BUY: self._setup_to_buy,
            consts.OrderSide.SELL: self._setup_to_sell,
        }[next_operation]

        return setup_func()

    @staticmethod
    def _get_next_operation():
        print('')
        print('')
        print('Please, indicate what should be the first operation. Choices = buy / sell')
        print('')
        operation_side = input('Insert the first operation: ')
        return str(operation_side).lower()

    def _setup_to_buy(self):
        start_value = self._get_start_value()
        reversal = self._get_trend_reversal()
        stop_loss = self._get_stop_loss()
        operational_cost = self._get_operational_cost()
        profit = self._get_profit()

        buy_price = utils.get_buy_price(start_value, reversal)
        sell_price = buy_price * (1 + ((operational_cost + profit) / 100))
        stop_value = (sell_price * 100) / (100 - reversal)

        return beans.TrailingOrderSetup.make(
            consts.OrderSide.BUY, start_value, stop_value, reversal, stop_loss, operational_cost, profit
        )

    def _setup_to_sell(self):
        stop_value = self._get_stop_value()
        reversal = self._get_trend_reversal()
        stop_loss = self._get_stop_loss()
        operational_cost = self._get_operational_cost()
        profit = self._get_profit()

        sell_price = utils.get_sell_price(stop_value, reversal)
        buy_price = sell_price * (1 - ((operational_cost + profit) / 100))
        start_value = (buy_price * 100) / (100 + reversal)
        return beans.TrailingOrderSetup.make(
            consts.OrderSide.SELL, start_value, stop_value, reversal, stop_loss, operational_cost, profit
        )

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
    def _get_trend_reversal():
        print('')
        print('')
        return float(input('Insert the trend reversal margin to place the order: '))

    @staticmethod
    def _get_stop_loss():
        print('')
        print('')
        print('If price continues to fall after the buy operation, it must be a good idea to put a STOP LOSS order '
              'to avoid loss more money.')
        print('When the price reach this limit, a selling order will be placed')
        print('Left it empty to skip stop loss setup')
        print('')
        return float(input('Insert the percentage to place the stop loss order: '))

    @staticmethod
    def _get_operational_cost():
        print('')
        print('')
        return float(input('Insert the total operational costs to buy and sell: '))

    @staticmethod
    def _get_profit():
        print('')
        print('')
        return float(input('Insert the desired minimum profit in each operation: '))
