from abc import ABCMeta, abstractmethod


class IOrderCommand(object):
    __metaclass__ = ABCMeta

    system = NotImplemented

    @abstractmethod
    def execute(self, last_quote):
        """
        :type last_quote: float
        """


class ITradingSystem(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def run(self):
        """
        :return: None
        """
