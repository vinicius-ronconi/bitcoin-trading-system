from unittest import TestCase

import mock

from trading_system import consts
from trading_system.systems.trailing_orders.commands import SellBitcoinsCommand


class TrailingOrdersTestCase(TestCase):
    def setUp(self):
        system = mock.MagicMock()
        self.command = SellBitcoinsCommand(system)
        self.command.system.next_operation = consts.OrderSide.SELL

    def test_it_places_a_sell_order(self):
        self.command.system.is_tracking = True
        self.command.system.sell_price = 1000.0
        self.command.system.stop_loss_price = 500.0
        self.command.execute(self.command.system.sell_price)
        self._assert_results(buy_call_count=0, sell_call_count=1, order_side=consts.OrderSide.BUY, is_tracking=False)

        self.command.system.reset_mock()

        self.command.system.is_tracking = True
        self.command.execute(self.command.system.sell_price - 0.01)
        self._assert_results(buy_call_count=0, sell_call_count=1, order_side=consts.OrderSide.BUY, is_tracking=False)

    def test_it_does_not_place_a_sell_order_besides_is_tracking(self):
        self.command.system.is_tracking = True
        self.command.system.sell_price = 1000.0
        self.command.system.stop_loss_price = 500.0
        self.command.execute(self.command.system.sell_price + 0.01)
        self._assert_results(buy_call_count=0, sell_call_count=0, order_side=consts.OrderSide.SELL, is_tracking=True)

    def test_it_starts_tracking_for_selling_purposes(self):
        self.command.system.is_tracking = False
        self.command.system.stop_value = 1000.0
        self.command.system.stop_loss_price = 500.0
        self.command.execute(self.command.system.stop_value)
        self._assert_results(buy_call_count=0, sell_call_count=0, order_side=consts.OrderSide.SELL, is_tracking=True)

        self.command.system.is_tracking = False
        self.command.execute(self.command.system.stop_value + 0.01)
        self._assert_results(buy_call_count=0, sell_call_count=0, order_side=consts.OrderSide.SELL, is_tracking=True)

    def test_it_does_not_start_tracking_for_selling_purposes(self):
        self.command.system.is_tracking = False
        self.command.system.stop_value = 1000.0
        self.command.system.stop_loss_price = 500.0
        self.command.execute(self.command.system.stop_value - 0.01)
        self._assert_results(buy_call_count=0, sell_call_count=0, order_side=consts.OrderSide.SELL, is_tracking=False)

    def test_it_stops_loss_when_not_tracking(self):
        self.command.system.is_tracking = False
        self.command.system.stop_value = 1000.0
        self.command.system.stop_loss_price = 500.0
        self.command.execute(self.command.system.stop_loss_price - 0.01)
        self._assert_results(buy_call_count=0, sell_call_count=1, order_side=consts.OrderSide.BUY, is_tracking=False)

    def test_it_does_not_stop_loss_when_not_tracking(self):
        self.command.system.is_tracking = False
        self.command.system.stop_value = 1000.0
        self.command.system.stop_loss_price = 500.0
        self.command.execute(self.command.system.stop_loss_price)
        self._assert_results(buy_call_count=0, sell_call_count=0, order_side=consts.OrderSide.SELL, is_tracking=False)

        self.command.execute(self.command.system.stop_loss_price + 0.01)
        self._assert_results(buy_call_count=0, sell_call_count=0, order_side=consts.OrderSide.SELL, is_tracking=False)

    def _assert_results(self, buy_call_count, sell_call_count, order_side, is_tracking):
        self.assertEqual(self.command.system.client.orders.buy_bitcoins.call_count, buy_call_count)
        self.assertEqual(self.command.system.client.orders.sell_bitcoins.call_count, sell_call_count)
        self.assertEqual(self.command.system.next_operation, order_side)
        self.assertEqual(self.command.system.is_tracking, is_tracking)
