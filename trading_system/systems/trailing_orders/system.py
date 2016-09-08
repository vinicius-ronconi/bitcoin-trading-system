import logging
import logging.handlers
import os

from trading_system import consts, settings
from trading_system.systems.interfaces import ITradingSystem
from trading_system.systems.trailing_orders import beans, commands, utils
from trading_system.utils import get_rounded_decimal_value

APP_LEVEL = 60
logging.addLevelName(APP_LEVEL, 'APP')
logger = logging.getLogger('')
logger.setLevel(logging.ERROR)

os.makedirs(settings.LOG_DIR, exist_ok=True)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

file_handler = logging.handlers.RotatingFileHandler(
    filename='{0}/{1}'.format(settings.LOG_DIR, 'trailing_orders_log.txt'),
    maxBytes=(1024*1024*10),
    backupCount=7
)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)


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

    def __init__(self, client, bootstrap):
        """
        :type client: trading_system.api.interfaces.IClient
        :type bootstrap: trading_system.systems.trailing_orders.interfaces.IBootStrap
        """
        self.client = client
        self.setup = bootstrap.get_initial_setup()
        self.is_tracking = False

        self.log_info('System started with the following values:')
        self.log_info('    Next Operation: {}'.format(self.setup.next_operation))
        self.log_info('    Start value: {}'.format(self.setup.start_value))
        self.log_info('    Buy Price: {}'.format(self.buy_price))
        self.log_info('    Sell Price: {}'.format(self.sell_price))
        self.log_info('    Stop value: {}'.format(self.setup.stop_value))
        self.log_info('    Reversal %: {}'.format(self.setup.reversal))
        self.log_info('')
        self.log_info('    Stop Loss %: {}'.format(self.setup.stop_loss))
        self.log_info('    Stop Loss Price: {}'.format(self.stop_loss_price))
        self.log_info('')
        self.log_info('    Gross Margin: {}'.format(
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
        logging.log(APP_LEVEL, text)

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
