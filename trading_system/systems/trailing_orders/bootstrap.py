from trading_system import consts
from trading_system.systems.trailing_orders import utils, beans
from trading_system.systems.trailing_orders.interfaces import IBootStrap
from trading_system.utils import get_rounded_decimal_value

class ManualInputBootstrap(IBootStrap):
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
        operational_cost = self._get_operational_cost()
        profit = self._get_profit()
        stop_loss = self._get_stop_loss()

        buy_price = utils.get_buy_price(start_value, reversal)
        sell_price = get_rounded_decimal_value(buy_price * (1 + ((operational_cost + profit) / 100)))
        stop_value = get_rounded_decimal_value((sell_price * 100) / (100 - reversal))

        return beans.TrailingOrderSetup.make(
            consts.OrderSide.BUY, start_value, stop_value, reversal, stop_loss, operational_cost, profit
        )

    def _setup_to_sell(self):
        stop_value = self._get_stop_value()
        reversal = self._get_trend_reversal()
        operational_cost = self._get_operational_cost()
        profit = self._get_profit()
        stop_loss = self._get_stop_loss()

        sell_price = utils.get_sell_price(stop_value, reversal)
        buy_price = get_rounded_decimal_value(sell_price * (1 - ((operational_cost + profit) / 100)))
        start_value = get_rounded_decimal_value((buy_price * 100) / (100 + reversal))
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


class FakeBootstrap(IBootStrap):
    def __init__(self, initial_setup):
        """
        :type initial_setup: trading_system.systems.trailing_orders.beans.TrailingOrderSetup
        """
        self.initial_setup_values = initial_setup

    def get_initial_setup(self):
        return self.initial_setup_values
