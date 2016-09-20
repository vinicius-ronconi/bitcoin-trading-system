import logging
import logging.handlers
import os

from trading_system import settings
from trading_system.systems.trailing_orders.interfaces import ITrailingOrdersSystem
from trading_system.systems.trailing_orders.factory import TrailingOrdersFactory
from trading_system.systems.trailing_orders import beans, utils
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


class TrailingOrders(ITrailingOrdersSystem):
    def __init__(self, client, bootstrap):
        """
        :type client: trading_system.api.interfaces.IClient
        :type bootstrap: trading_system.systems.trailing_orders.interfaces.IBootStrap
        """
        self.client = client
        self.setup = bootstrap.get_initial_setup()
        self.is_tracking = False
        self.state = TrailingOrdersFactory().make_state_by_setup(self)

        self.log_info('System started with the following values:')
        self.print_current_values()

    @property
    def buy_price(self):
        return utils.get_buy_price(self.setup.start_value, self.setup.reversal)

    @property
    def sell_price(self):
        return utils.get_sell_price(self.setup.stop_value, self.setup.reversal)

    @property
    def stop_loss_price(self):
        return utils.get_stop_loss_price(self.setup.start_value, self.setup.stop_loss)

    def set_state(self, state):
        self.state = state

    def run(self):
        self.update_balance()
        self.current_ticker = self.get_current_ticker()
        self.state.evaluate_last_quote(self.current_ticker.last_value)

    def update_balance(self):
        self.balance = self.client.account.get_balance()
        return self.balance

    def get_current_ticker(self):
        return self.client.market.get_ticker()

    def get_pending_orders(self):
        return self.client.orders.get_pending_orders(page=0, page_size=5)

    @staticmethod
    def log_info(text):
        logging.log(APP_LEVEL, text)

    def set_next_operation(self, next_operation):
        self.update_setup(
            beans.TrailingOrderSetup(
                next_operation=next_operation,
                start_value=self.setup.start_value,
                stop_value=self.setup.stop_value,
                reversal=self.setup.reversal,
                stop_loss=self.setup.stop_loss,
                operational_cost=self.setup.operational_cost,
                profit=self.setup.profit,
            )
        )

    def update_setup(self, setup):
        self.setup = setup

    def print_current_values(self):
        self.log_info('    Next Operation: {}'.format(self.setup.next_operation))
        self.log_info('    Reversal %: {}'.format(self.setup.reversal))
        self.log_info('')
        self.log_info('    Start value: {}'.format(self.setup.start_value))
        self.log_info('    Buy Price: {}'.format(self.buy_price))
        self.log_info('    Sell Price: {}'.format(self.sell_price))
        self.log_info('    Stop value: {}'.format(self.setup.stop_value))
        self.log_info('')
        self.log_info('    Stop Loss %: {}'.format(self.setup.stop_loss))
        self.log_info('    Stop Loss Price: {}'.format(self.stop_loss_price))
        self.log_info('')
        self.log_info('    Gross Margin: {}'.format(
            get_rounded_decimal_value(((self.sell_price / self.buy_price) - 1) * 100))
        )
