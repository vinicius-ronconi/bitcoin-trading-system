from unittest import TestCase

import mock

from trading_system import consts
from trading_system.systems.trailing_orders import TrailingOrders
from trading_system.systems.trailing_orders.beans import TrailingOrderSetup


class TrailingOrdersTestCase(TestCase):
    START_VALUE = 100.0
    STOP_VALUE = 200.0
    REVERSAL = 5
    STOP_LOSS = 10

    system_setup = NotImplemented
    system = NotImplemented

    def test_it_update_start_stop_values_during_buy_operation(self):
        self._setup_operation(consts.OrderSide.BUY)
        last_quote = self.START_VALUE / 2
        self.system.update_start_stop_values_if_necessary(last_quote)
        self.assertEqual(self.system.setup.start_value, last_quote)
        self.assertEqual(self.system.setup.stop_value, self.STOP_VALUE * (last_quote / self.START_VALUE))

    def test_it_update_start_stop_values_during_sell_operation(self):
        self._setup_operation(consts.OrderSide.SELL)
        last_quote = self.STOP_VALUE * 2
        self.system.update_start_stop_values_if_necessary(last_quote)
        self.assertEqual(self.system.setup.start_value, self.START_VALUE * 2)
        self.assertEqual(self.system.setup.stop_value, last_quote)

    def test_it_does_not_update_start_stop_values(self):
        self._setup_operation(consts.OrderSide.BUY)
        self.system_setup.reset_mock()
        last_quote = self.STOP_VALUE * 2
        self.system.update_start_stop_values_if_necessary(last_quote)
        self.assertEqual(self.system.setup.start_value, self.START_VALUE)
        self.assertEqual(self.system.setup.stop_value, self.STOP_VALUE)

        self._setup_operation(consts.OrderSide.SELL)
        last_quote = (self.START_VALUE + self.STOP_VALUE) / 2
        self.system.update_start_stop_values_if_necessary(last_quote)
        self.assertEqual(self.system.setup.start_value, self.START_VALUE)
        self.assertEqual(self.system.setup.stop_value, self.STOP_VALUE)

        self._setup_operation(consts.OrderSide.SELL)
        last_quote = self.START_VALUE / 2
        self.system.update_start_stop_values_if_necessary(last_quote)
        self.assertEqual(self.system.setup.start_value, self.START_VALUE)
        self.assertEqual(self.system.setup.stop_value, self.STOP_VALUE)

    @mock.patch('trading_system.systems.trailing_orders.commands.BuyBitcoinsCommand.execute')
    def test_it_calls_buy_command(self, command):
        self._setup_operation(consts.OrderSide.BUY)
        self.system.client.orders.get_pending_orders.return_value = []
        self.system.update_start_stop_values_if_necessary = mock.Mock()
        self.system.run()
        self.assertEqual(command.call_count, 1)

    @mock.patch('trading_system.systems.trailing_orders.commands.SellBitcoinsCommand.execute')
    def test_it_calls_sell_command(self, command):
        self._setup_operation(consts.OrderSide.SELL)
        self.system.client.orders.get_pending_orders.return_value = []
        self.system.update_start_stop_values_if_necessary = mock.Mock()
        self.system.run()
        self.assertEqual(command.call_count, 1)

    @mock.patch('trading_system.systems.trailing_orders.commands.EvaluatePendingOrdersCommand.execute')
    def test_it_calls_pending_orders_command(self, command):
        self._setup_operation(consts.OrderSide.SELL)
        self.system.client.orders.get_pending_orders.return_value = ['any_fake_content']
        self.system.update_start_stop_values_if_necessary = mock.Mock()
        self.system.run()
        self.assertEqual(command.call_count, 1)

        self.system.run()
        self.assertEqual(command.call_count, 2)

    def test_it_gets_buy_price(self):
        self._setup_operation(consts.OrderSide.BUY)
        self.assertEqual(self.system.buy_price, 105.0)

    def test_it_gets_sell_price(self):
        self._setup_operation(consts.OrderSide.SELL)
        self.assertEqual(self.system.sell_price, 190.0)

    def test_it_gets_stop_loss_price(self):
        self._setup_operation(consts.OrderSide.SELL)
        self.assertEqual(self.system.stop_loss_price, 90.0)

    def test_it_setup_buy_operation(self):
        self._setup_next_operation(consts.OrderSide.BUY)
        self._setup_start_value(100)
        self._setup_reversal(1)
        self._setup_stop_loss(2)
        self._setup_operational_cost(1)
        self._setup_profit(1)

        client = mock.Mock()
        self.system = TrailingOrders(client)

        self.assertEqual(self.system.setup.stop_value, 104.06)
        self.assertEqual(self.system.buy_price, 101)
        self.assertEqual(self.system.sell_price, 103.01)
        self.assertEqual(self.system.stop_loss_price, 98)

    def test_it_setup_sell_operation(self):
        self._setup_next_operation(consts.OrderSide.SELL)
        self._setup_stop_value(100)
        self._setup_reversal(1)
        self._setup_stop_loss(2)
        self._setup_operational_cost(1)
        self._setup_profit(1)

        client = mock.Mock()
        self.system = TrailingOrders(client)

        self.assertEqual(self.system.setup.start_value, 96.05)
        self.assertEqual(self.system.sell_price, 99)
        self.assertEqual(self.system.buy_price, 97.01)
        self.assertEqual(self.system.stop_loss_price, 94.12)

    def test_it_sets_next_operation(self):
        self._setup_next_operation(consts.OrderSide.BUY)
        self._setup_start_value(100)
        self._setup_reversal(1)
        self._setup_stop_loss(2)
        self._setup_operational_cost(1)
        self._setup_profit(1)

        client = mock.Mock()
        self.system = TrailingOrders(client)
        self.system.set_next_operation(consts.OrderSide.SELL)

        self.assertEqual(self.system.setup.next_operation, consts.OrderSide.SELL)

        self.system.set_next_operation(consts.OrderSide.BUY)
        self.assertEqual(self.system.setup.next_operation, consts.OrderSide.BUY)

    def _setup_next_operation(self, next_operation):
        self.next_operation = mock.MagicMock(return_value=next_operation)
        next_operation_patcher = mock.patch(
            'trading_system.systems.trailing_orders.TrailingOrders._get_next_operation', self.next_operation
        )
        self.addCleanup(next_operation_patcher.stop)
        next_operation_patcher.start()

    def _setup_start_value(self, value):
        self.start_value = mock.MagicMock(return_value=value)
        start_value_patcher = mock.patch(
            'trading_system.systems.trailing_orders.TrailingOrders._get_start_value', self.start_value
        )
        self.addCleanup(start_value_patcher.stop)
        start_value_patcher.start()

    def _setup_stop_value(self, value):
        self.stop_value = mock.MagicMock(return_value=value)
        stop_value_patcher = mock.patch(
            'trading_system.systems.trailing_orders.TrailingOrders._get_stop_value', self.stop_value
        )
        self.addCleanup(stop_value_patcher.stop)
        stop_value_patcher.start()

    def _setup_reversal(self, value):
        self.reversal = mock.MagicMock(return_value=value)
        reversal_patcher = mock.patch(
            'trading_system.systems.trailing_orders.TrailingOrders._get_trend_reversal', self.reversal
        )
        self.addCleanup(reversal_patcher.stop)
        reversal_patcher.start()

    def _setup_stop_loss(self, value):
        self.stop_loss = mock.MagicMock(return_value=value)
        stop_loss_patcher = mock.patch(
            'trading_system.systems.trailing_orders.TrailingOrders._get_stop_loss', self.stop_loss
        )
        self.addCleanup(stop_loss_patcher.stop)
        stop_loss_patcher.start()

    def _setup_operational_cost(self, value):
        self.operational_cost = mock.MagicMock(return_value=value)
        operational_cost_patcher = mock.patch(
            'trading_system.systems.trailing_orders.TrailingOrders._get_operational_cost', self.operational_cost
        )
        self.addCleanup(operational_cost_patcher.stop)
        operational_cost_patcher.start()

    def _setup_profit(self, value):
        self.profit = mock.MagicMock(return_value=value)
        profit_patcher = mock.patch(
            'trading_system.systems.trailing_orders.TrailingOrders._get_profit', self.profit
        )
        self.addCleanup(profit_patcher.stop)
        profit_patcher.start()

    def _setup_operation(self, next_operation):
        self.system_setup = mock.MagicMock(return_value=TrailingOrderSetup(
            next_operation=next_operation,
            start_value=self.START_VALUE,
            stop_value=self.STOP_VALUE,
            reversal=self.REVERSAL,
            stop_loss=self.STOP_LOSS,
            operational_cost=0.2,
            profit=0.5,
        ))
        setup_patcher = mock.patch(
            'trading_system.systems.trailing_orders.TrailingOrders._setup_values', self.system_setup
        )
        self.addCleanup(setup_patcher.stop)
        setup_patcher.start()

        client = mock.Mock()
        self.system = TrailingOrders(client)
