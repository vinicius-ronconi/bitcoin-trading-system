from abc import ABCMeta, abstractmethod
from trading_system.systems.interfaces import ITradingSystem


class ITrailingOrdersSystem(ITradingSystem):
    """
    :type client: trading_system.api.interfaces.IClient
    :type setup: trading_system.systems.trailing_orders.beans.TrailingOrderSetup
    :type is_tracking: bool
    :type balance: trading_system.api.beans.Balance
    :type current_ticker: trading_system.api.beans.Ticker
    """

    __metaclass__ = ABCMeta

    client = NotImplemented
    setup = NotImplemented
    is_tracking = NotImplemented
    balance = NotImplemented
    current_ticker = NotImplemented

    @abstractmethod
    def run(self):
        """
        :rtype: -
        """

    @abstractmethod
    def get_pending_orders(self):
        """
        :rtype: list[trading_system.api.beans.PlacedOrder]
        """

    @abstractmethod
    def update_balance(self):
        """
        :rtype: trading_system.api.beans.Balance
        """

    @staticmethod
    @abstractmethod
    def log_info(text):
        """
        :type text: basestring
        """

    @abstractmethod
    def print_current_values(self):
        """
        :rtype: -
        """

    @abstractmethod
    def set_state(self, state):
        """
        :type state: trading_system.systems.trailing_orders.interfaces.ISystemState
        """

    @abstractmethod
    def set_next_operation(self, next_operation):
        """
        :type next_operation: basestring
        """
    @abstractmethod
    def update_setup(self, setup):
        """
        :type setup: trading_system.systems.trailing_orders.beans.TrailingOrderSetup
        """

    @property
    @abstractmethod
    def buy_price(self):
        """
        :rtype: float
        """

    @property
    @abstractmethod
    def sell_price(self):
        """
        :rtype: float
        """

    @property
    @abstractmethod
    def stop_loss_price(self):
        """
        :rtype: float
        """


class ISystemState(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def evaluate_last_quote(self, last_quote):
        """
        :type last_quote: float
        """


class IBootStrap(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_initial_setup(self):
        """
        :rtype: trading_system.systems.trailing_orders.beans.TrailingOrderSetup
        """
