from abc import ABCMeta, abstractmethod


class IAccountApi(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_balance(self):
        """
        :rtype: trading_system.api.beans.Balance
        """


class IClient(object):
    """
    :type account: trading_system.api.interfaces.IAccountApi
    :type market: trading_system.api.interfaces.IMarketApi
    :type orders: trading_system.api.interfaces.IOrdersApi
    """
    __metaclass__ = ABCMeta

    account = NotImplemented
    market = NotImplemented
    orders = NotImplemented

    @staticmethod
    @abstractmethod
    def get_currency_value(satoshi):
        """
        :type satoshi: long
        :rtype: float
        """

    @staticmethod
    @abstractmethod
    def get_satoshi_value(value):
        """
        :type value: float
        :rtype: long
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
        :rtype: list[trading_system.api.beans.PlacedOrder|trading_system.api.beans.Balance]
        """

    @abstractmethod
    def cancel_order(self, order_id):
        """
        :type order_id: basestring
        :rtype: list[trading_system.api.beans.PlacedOrder|trading_system.api.beans.Balance]
        """

    @abstractmethod
    def get_pending_orders(self, page, page_size):
        """
        :type page: long
        :type page_size: long
        :rtype: list[trading_system.api.beans.PlacedOrder]
        """

    @abstractmethod
    def get_executed_orders(self, page, page_size):
        """
        :type page: long
        :type page_size: long
        :rtype: list[trading_system.api.beans.PlacedOrder]
        """