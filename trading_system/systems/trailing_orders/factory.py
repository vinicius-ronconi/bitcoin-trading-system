from trading_system import consts
from trading_system.systems.trailing_orders.bootstrap import ManualInputBootstrap, FakeBootstrap
from trading_system.systems.trailing_orders import states


class TrailingOrdersFactory(object):
    @staticmethod
    def make_input_bootstrap():
        return ManualInputBootstrap()

    @staticmethod
    def make_fake_bootstrap(initial_setup):
        return FakeBootstrap(initial_setup)

    @staticmethod
    def make_state_by_setup(system):
        """
        :type system: trading_system.systems.trailing_orders.interfaces.ITrailingOrdersSystem
        :rtype: trading_system.systems.trailing_orders.interfaces.ISystemState
        """
        if system.setup.next_operation == consts.OrderSide.BUY:
            return states.WaitingToBuyState(system)
        elif system.setup.next_operation == consts.OrderSide.SELL:
            return states.WaitingToSellState(system)
