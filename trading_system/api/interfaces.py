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

    open_api = NotImplemented
    auth_api = NotImplemented

    account = NotImplemented
    market = NotImplemented
    orders = NotImplemented


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
    def get_trade_list(self, since_ts):
        """
        :type since_ts: int
        :rtype: list[trading_system.api.beans.Trade]
        """


class IOrdersApi(object):
    __metaclass__ = ABCMeta

    # TODO: Add market orders
    @abstractmethod
    def buy_bitcoins_with_limited_order(self, price, quantity):
        """
        :type price: float
        :type quantity: float
        :rtype: list[trading_system.api.beans.PlacedOrder|trading_system.api.beans.Balance]
        """

    @abstractmethod
    def sell_bitcoins_with_limited_order(self, price, quantity):
        """
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
        :type page: int
        :type page_size: int
        :rtype: list[trading_system.api.beans.PlacedOrder]
        """
