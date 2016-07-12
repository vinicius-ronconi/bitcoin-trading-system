from unittest import TestCase
import mock
from trading_system.api import beans, consts
from trading_system.systems.trailing_orders import TrailingOrders


class TrailingOrdersTestCase(TestCase):
    CURRENT_BALANCE = 10000
    START_VALUE = 2000
    STOP_VALUE = 2500
    ORDER_PLACEMENT_PERC = 1.5
    STOP_LOSS_TRIGGER = 2

    def setUp(self):
        self.get_start_value_method = mock.MagicMock(return_value=self.START_VALUE)
        start_value_patcher = mock.patch(
            'trading_system.systems.trailing_orders.TrailingOrders._get_start_value', self.get_start_value_method
        )
        self.addCleanup(start_value_patcher.stop)
        start_value_patcher.start()

        self.get_stop_value_method = mock.MagicMock(return_value=self.STOP_VALUE)
        stop_value_patcher = mock.patch(
            'trading_system.systems.trailing_orders.TrailingOrders._get_stop_value', self.get_stop_value_method
        )
        self.addCleanup(stop_value_patcher.stop)
        stop_value_patcher.start()

        self.get_order_placement_perc_method = mock.MagicMock(return_value=self.ORDER_PLACEMENT_PERC)
        order_placement_perc_patcher = mock.patch(
            'trading_system.systems.trailing_orders.TrailingOrders._get_order_placement_percentage',
            self.get_order_placement_perc_method
        )
        self.addCleanup(order_placement_perc_patcher.stop)
        order_placement_perc_patcher.start()

        self.stop_loss_trigger_method = mock.MagicMock(return_value=self.STOP_LOSS_TRIGGER)
        stop_loss_trigger_patcher = mock.patch(
            'trading_system.systems.trailing_orders.TrailingOrders._get_stop_loss_trigger',
            self.stop_loss_trigger_method
        )
        self.addCleanup(stop_loss_trigger_patcher.stop)
        stop_loss_trigger_patcher.start()

        self.next_operation_method = mock.MagicMock(return_value=consts.OrderSide.BUY)
        order_side_patcher = mock.patch(
            'trading_system.systems.trailing_orders.TrailingOrders._get_next_operation',
            self.next_operation_method
        )
        self.addCleanup(order_side_patcher.stop)
        order_side_patcher.start()

        self.system = TrailingOrders()

    def test_it_places_a_buy_order(self):
        self._set_up_for_buying_purposes(self._get_order_placement_value(), self.CURRENT_BALANCE, is_tracking=True)
        self.system.run()
        self._assert_results(buy_call_count=1, sell_call_count=0, order_side=consts.OrderSide.SELL, is_tracking=False)

    def _get_order_placement_value(self):
        return round(self.START_VALUE * ((100 + self.ORDER_PLACEMENT_PERC) / 100), 2)

    def _set_up_for_buying_purposes(self, last_value, current_balance, is_tracking):
        self.system.is_tracking = is_tracking
        self.system.client = mock.Mock()
        self.system.client.orders.get_pending_orders.return_value = []
        self.system.client.account.get_balance.return_value = beans.Balance(
            currency=current_balance, currency_locked=0, btc=0, btc_locked=0,
        )
        self.system.client.get_satoshi_value.return_value = int((current_balance / last_value) * 100000000)
        self.system.client.market.get_ticker.return_value = beans.Ticker(
            last_value=last_value,
            currency_pair='BTCBRL', highest_value=2300, lowest_value=2200, best_sell_order=2205, best_buy_order=2195,
            volume_btc=200, volume_currency=400000,
        )

    def _assert_results(self, buy_call_count, sell_call_count, order_side, is_tracking):
        self.assertEqual(self.system.client.orders.buy_bitcoins.call_count, buy_call_count)
        self.assertEqual(self.system.client.orders.sell_bitcoins.call_count, sell_call_count)
        self.assertEqual(self.system.next_operation, order_side)
        self.assertEqual(self.system.is_tracking, is_tracking)

    def test_it_does_not_place_a_buy_order_besides_is_tracking(self):
        self._set_up_for_buying_purposes(
            self._get_order_placement_value() - 0.01, self.CURRENT_BALANCE, is_tracking=True
        )
        self.system.run()
        self._assert_results(buy_call_count=0, sell_call_count=0, order_side=consts.OrderSide.BUY, is_tracking=True)

    def test_it_starts_tracking(self):
        self._set_up_for_buying_purposes(self.START_VALUE, self.CURRENT_BALANCE, is_tracking=False)
        self.system.run()
        self._assert_results(buy_call_count=0, sell_call_count=0, order_side=consts.OrderSide.BUY, is_tracking=True)

    def test_it_does_not_start_tracking(self):
        self._set_up_for_buying_purposes(self.START_VALUE + 0.01, self.CURRENT_BALANCE, is_tracking=False)
        self.system.run()
        self._assert_results(buy_call_count=0, sell_call_count=0, order_side=consts.OrderSide.BUY, is_tracking=False)
