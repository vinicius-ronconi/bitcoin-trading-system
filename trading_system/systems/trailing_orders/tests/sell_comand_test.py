from unittest import TestCase

import mock

from trading_system import consts
from trading_system.api.beans import Ticker
from trading_system.systems.trailing_orders.system import TrailingOrders
from trading_system.systems.trailing_orders import beans


class TrailingOrdersTestCase(TestCase):
    def setUp(self):
        self.mocked_setup = mock.MagicMock(return_value=beans.TrailingOrderSetup(
            next_operation=consts.OrderSide.SELL,
            start_value=100,
            stop_value=200,
            reversal=10,
            stop_loss=20,
            operational_cost=1,
            profit=2,
        ))
        setup_patcher = mock.patch(
            'trading_system.systems.trailing_orders.system.SystemBootstrap.get_initial_setup', self.mocked_setup
        )
        self.addCleanup(setup_patcher.stop)
        setup_patcher.start()

        client = mock.MagicMock()
        self.system = TrailingOrders(client)
        self.system.log_info = mock.MagicMock()
        self.system._get_pending_orders = mock.MagicMock(return_value=[])

        self.set_next_operation = mock.MagicMock()
        next_operation_patcher = mock.patch(
            'trading_system.systems.trailing_orders.system.TrailingOrders.set_next_operation', self.set_next_operation
        )
        self.addCleanup(next_operation_patcher.stop)
        next_operation_patcher.start()

    def test_it_places_a_sell_order(self):
        self.system.is_tracking = True
        self._set_last_quote(self.system.sell_price)
        self.system.run()
        self._assert_results(sell_call_count=1, is_tracking=False)
        self.assertEqual(self.set_next_operation.call_args[0][0], consts.OrderSide.BUY)

        self.system.is_tracking = True
        self._set_last_quote(self.system.sell_price - 0.01)
        self.system.run()
        self._assert_results(sell_call_count=2, is_tracking=False)
        self.assertEqual(self.set_next_operation.call_args[0][0], consts.OrderSide.BUY)

    def test_it_does_not_place_a_sell_order_besides_is_tracking(self):
        self.system.is_tracking = True
        self._set_last_quote(self.system.sell_price + 0.01)
        self.system.run()
        self._assert_results(sell_call_count=0, is_tracking=True)

    def test_it_starts_tracking_for_selling_purposes(self):
        self.system.is_tracking = False
        self._set_last_quote(self.system.setup.stop_value)
        self.system.run()
        self._assert_results(sell_call_count=0, is_tracking=True)

        self.system.is_tracking = False
        self._set_last_quote(self.system.setup.stop_value + 0.01)
        self.system.run()
        self._assert_results(sell_call_count=0, is_tracking=True)

    def test_it_does_not_start_tracking_for_selling_purposes(self):
        self.system.is_tracking = False
        self._set_last_quote(self.system.setup.stop_value - 0.01)
        self.system.run()
        self._assert_results(sell_call_count=0, is_tracking=False)

    def test_it_stops_loss_when_not_tracking(self):
        self.system.is_tracking = False
        self._set_last_quote(self.system.stop_loss_price - 0.01)
        self.system.run()
        self._assert_results(sell_call_count=1, is_tracking=True)
        self.assertEqual(self.set_next_operation.call_args[0][0], consts.OrderSide.BUY)

    def test_it_does_not_stop_loss_when_not_tracking(self):
        self.system.is_tracking = False
        self._set_last_quote(self.system.stop_loss_price)
        self.system.run()
        self._assert_results(sell_call_count=0, is_tracking=False)

        self.system.is_tracking = False
        self._set_last_quote(self.system.stop_loss_price + 0.01)
        self.system.run()
        self._assert_results(sell_call_count=0, is_tracking=False)

    def _set_last_quote(self, last_quote):
        self.system._get_current_ticker = mock.MagicMock(return_value=Ticker(
            currency_pair='BTCUSD',
            last_value=last_quote,
            highest_value=200.0,
            lowest_value=100.0,
            best_sell_order=140.0,
            best_buy_order=120.0,
            volume_btc=100,
            volume_currency=100,
        ))

    def _assert_results(self, sell_call_count, is_tracking):
        self.assertEqual(self.system.client.orders.buy_bitcoins_with_limited_order.call_count, 0)
        self.assertEqual(self.system.client.orders.sell_bitcoins_with_limited_order.call_count, sell_call_count)
        self.assertEqual(self.set_next_operation.call_count, sell_call_count)
        self.assertEqual(self.system.is_tracking, is_tracking)
