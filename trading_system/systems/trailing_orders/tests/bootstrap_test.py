from unittest import TestCase

import mock

from trading_system import consts
from trading_system.systems.trailing_orders.bootstrap import ManualInputBootstrap


class ManualInputBootStrapTestCase(TestCase):
    def setUp(self):
        self._setup_reversal(1)
        self._setup_stop_loss(2)
        self._setup_operational_cost(1)
        self._setup_profit(1)

    def test_it_setup_buy_operation(self):
        self._setup_next_operation(consts.OrderSide.BUY)
        self._setup_start_value(100)
        initial_setup = ManualInputBootstrap().get_initial_setup()
        self.assertEqual(initial_setup.stop_value, 104.06)

    def test_it_setup_sell_operation(self):
        self._setup_next_operation(consts.OrderSide.SELL)
        self._setup_stop_value(100)
        initial_setup = ManualInputBootstrap().get_initial_setup()
        self.assertEqual(initial_setup.start_value, 96.05)

    def _setup_next_operation(self, next_operation):
        self.next_operation = mock.MagicMock(return_value=next_operation)
        next_operation_patcher = mock.patch(
            'trading_system.systems.trailing_orders.bootstrap.ManualInputBootstrap._get_next_operation',
            self.next_operation
        )
        self.addCleanup(next_operation_patcher.stop)
        next_operation_patcher.start()

    def _setup_start_value(self, value):
        self.start_value = mock.MagicMock(return_value=value)
        start_value_patcher = mock.patch(
            'trading_system.systems.trailing_orders.bootstrap.ManualInputBootstrap._get_start_value', self.start_value
        )
        self.addCleanup(start_value_patcher.stop)
        start_value_patcher.start()

    def _setup_stop_value(self, value):
        self.stop_value = mock.MagicMock(return_value=value)
        stop_value_patcher = mock.patch(
            'trading_system.systems.trailing_orders.bootstrap.ManualInputBootstrap._get_stop_value', self.stop_value
        )
        self.addCleanup(stop_value_patcher.stop)
        stop_value_patcher.start()

    def _setup_reversal(self, value):
        self.reversal = mock.MagicMock(return_value=value)
        reversal_patcher = mock.patch(
            'trading_system.systems.trailing_orders.bootstrap.ManualInputBootstrap._get_trend_reversal', self.reversal
        )
        self.addCleanup(reversal_patcher.stop)
        reversal_patcher.start()

    def _setup_stop_loss(self, value):
        self.stop_loss = mock.MagicMock(return_value=value)
        stop_loss_patcher = mock.patch(
            'trading_system.systems.trailing_orders.bootstrap.ManualInputBootstrap._get_stop_loss', self.stop_loss
        )
        self.addCleanup(stop_loss_patcher.stop)
        stop_loss_patcher.start()

    def _setup_operational_cost(self, value):
        self.operational_cost = mock.MagicMock(return_value=value)
        operational_cost_patcher = mock.patch(
            'trading_system.systems.trailing_orders.bootstrap.ManualInputBootstrap._get_operational_cost',
            self.operational_cost
        )
        self.addCleanup(operational_cost_patcher.stop)
        operational_cost_patcher.start()

    def _setup_profit(self, value):
        self.profit = mock.MagicMock(return_value=value)
        profit_patcher = mock.patch(
            'trading_system.systems.trailing_orders.bootstrap.ManualInputBootstrap._get_profit', self.profit
        )
        self.addCleanup(profit_patcher.stop)
        profit_patcher.start()
