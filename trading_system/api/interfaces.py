from abc import ABCMeta, abstractmethod


class IAccountApi(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_balance(self):
        """
        :rtype: trading_system.api.beans.Balance
        """


class IMarketApi(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_ticker(self):
        """
        :rtype: trading_system.api.beans.Ticker
        """

    @abstractmethod
    def get_order_book(self):
        """
        :rtype: trading_system.api.beans.OrderBook
        """

    @abstractmethod
    def get_trade_list(self, offset):
        """
        :rtype: list[trading_system.api.beans.Trade]
        """


class IOrdersApi(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def buy_bitcoins(self, order_type, price, quantity):
        """
        :type order_type: basestring
        :type price: float
        :type quantity: float
        :rtype: list[trading_system.api.beans.PlacedOrder|trading_system.api.beans.Balance]
        """

    @abstractmethod
    def sell_bitcoins(self, order_type, price, quantity):
        """
        :type order_type: basestring
        :type price: float
        :type quantity: float
        :rtype: dict  # TODO Create a bean
        """

    @abstractmethod
    def cancel_order(self, order_id):
        """
        :param order_id: basestring
        :return: dict  # TODO Create a bean
        """
