from unittest import TestCase

import mock

from trading_system import consts
from trading_system.systems.trailing_orders.commands import BuyBitcoinsCommand


class TrailingOrdersTestCase(TestCase):
    def setUp(self):
        system = mock.MagicMock()
        self.command = BuyBitcoinsCommand(system)
        self.command.system.setup.next_operation = consts.OrderSide.BUY

    def test_it_places_a_buy_order(self):
        self.command.system.is_tracking = True
        self.command.system.buy_price = 1000.0
        self.command.execute(self.command.system.buy_price)
        self._assert_results(buy_call_count=1, is_tracking=False)
        self.assertEqual(self.command.system.set_next_operation.call_args[0][0], consts.OrderSide.SELL)

        self.command.system.reset_mock()

        self.command.system.is_tracking = True
        self.command.execute(self.command.system.buy_price + 0.01)
        self._assert_results(buy_call_count=1, is_tracking=False)
        self.assertEqual(self.command.system.set_next_operation.call_args[0][0], consts.OrderSide.SELL)

    def test_it_does_not_place_a_buy_order_besides_is_tracking(self):
        self.command.system.is_tracking = True
        self.command.system.buy_price = 1000.0
        self.command.execute(self.command.system.buy_price - 0.01)
        self._assert_results(buy_call_count=0, is_tracking=True)

    def test_it_starts_tracking(self):
        self.command.system.is_tracking = False
        self.command.system.setup.start_value = 1000.0
        self.command.execute(self.command.system.setup.start_value)
        self._assert_results(buy_call_count=0, is_tracking=True)

        self.command.system.is_tracking = False
        self.command.execute(self.command.system.setup.start_value - 0.01)
        self._assert_results(buy_call_count=0, is_tracking=True)

    def test_it_does_not_start_tracking(self):
        self.command.system.is_tracking = False
        self.command.system.setup.start_value = 1000.0
        self.command.execute(self.command.system.setup.start_value + 0.01)
        self._assert_results(buy_call_count=0, is_tracking=False)

    def _assert_results(self, buy_call_count, is_tracking):
        self.assertEqual(self.command.system.client.orders.buy_bitcoins_with_limited_order.call_count, buy_call_count)
        self.assertEqual(self.command.system.client.orders.sell_bitcoins_with_limited_order.call_count, 0)
        self.assertEqual(self.command.system.set_next_operation.call_count, buy_call_count)
        self.assertEqual(self.command.system.is_tracking, is_tracking)
