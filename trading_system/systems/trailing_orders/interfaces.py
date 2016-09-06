from abc import ABCMeta, abstractmethod


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
