from abc import ABCMeta, abstractmethod


class ITradingSystem(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def run(self):
        pass
