from unittest import TestCase
import mock
from trading_system.api import beans, consts
from trading_system.api.interfaces import IClient
from trading_system.systems.trailing_orders import TrailingOrders


class TrailingOrdersTestCase(TestCase):
    CURRENT_BALANCE = 10000.0
    START_VALUE = 2000.0
    STOP_VALUE = 2500.0
    ORDER_PLACEMENT_PERC = 1.5
    STOP_LOSS_TRIGGER = 2.0

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

    def test_it_places_a_buy_order(self):
        self._set_up_for_buying_purposes(self._get_buy_order_value(), self.CURRENT_BALANCE, is_tracking=True)
        self.system.run()
        self._assert_results(buy_call_count=1, sell_call_count=0, order_side=consts.OrderSide.SELL, is_tracking=False)

    def _get_buy_order_value(self):
        return round(self.START_VALUE * ((100 + self.ORDER_PLACEMENT_PERC) / 100), 2)

    def _set_up_for_buying_purposes(self, last_value, current_balance, is_tracking):
        self.next_operation_method = mock.MagicMock(return_value=consts.OrderSide.BUY)
        order_side_patcher = mock.patch(
            'trading_system.systems.trailing_orders.TrailingOrders._get_next_operation',
            self.next_operation_method
        )
        self.addCleanup(order_side_patcher.stop)
        order_side_patcher.start()

        client = mock.Mock(IClient)
        self.system = TrailingOrders(client)

        self.system.is_tracking = is_tracking
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
            self._get_buy_order_value() - 0.01, self.CURRENT_BALANCE, is_tracking=True
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

    def test_it_places_a_sell_order(self):
        self._set_up_for_selling_purposes(self._get_sell_order_value(), self.CURRENT_BALANCE, is_tracking=True)
        self.system.run()
        self._assert_results(buy_call_count=0, sell_call_count=1, order_side=consts.OrderSide.BUY, is_tracking=False)

    def _get_sell_order_value(self):
        return round(self.STOP_VALUE * ((100 - self.ORDER_PLACEMENT_PERC) / 100), 2)

    def _set_up_for_selling_purposes(self, last_value, btc_balance, is_tracking):
        self.next_operation_method = mock.MagicMock(return_value=consts.OrderSide.SELL)
        order_side_patcher = mock.patch(
            'trading_system.systems.trailing_orders.TrailingOrders._get_next_operation',
            self.next_operation_method
        )
        self.addCleanup(order_side_patcher.stop)
        order_side_patcher.start()

        client = mock.Mock(IClient)
        self.system = TrailingOrders(client)

        self.system.is_tracking = is_tracking
        self.system.client.orders.get_pending_orders.return_value = []
        self.system.client.account.get_balance.return_value = beans.Balance(
            currency=0, currency_locked=0, btc=btc_balance, btc_locked=0,
        )
        self.system.client.market.get_ticker.return_value = beans.Ticker(
            last_value=last_value,
            currency_pair='BTCBRL', highest_value=2300, lowest_value=2200, best_sell_order=2205, best_buy_order=2195,
            volume_btc=200, volume_currency=400000,
        )

    def test_it_does_not_place_a_sell_order_besides_is_tracking(self):
        self._set_up_for_selling_purposes(
            self._get_sell_order_value() + 0.01, self.CURRENT_BALANCE, is_tracking=True
        )
        self.system.run()
        self._assert_results(buy_call_count=0, sell_call_count=0, order_side=consts.OrderSide.SELL, is_tracking=True)

    def test_it_starts_tracking_for_selling_purposes(self):
        self._set_up_for_selling_purposes(self.STOP_VALUE, self.CURRENT_BALANCE, is_tracking=False)
        self.system.run()
        self._assert_results(buy_call_count=0, sell_call_count=0, order_side=consts.OrderSide.SELL, is_tracking=True)

    def test_it_does_not_start_tracking_for_selling_purposes(self):
        self._set_up_for_selling_purposes(self.STOP_VALUE - 0.01, self.CURRENT_BALANCE, is_tracking=False)
        self.system.run()
        self._assert_results(buy_call_count=0, sell_call_count=0, order_side=consts.OrderSide.SELL, is_tracking=False)

    def test_it_update_start_stop_values_if_necessary(self):
        self._set_up_for_selling_purposes(self.STOP_VALUE - 0.01, self.CURRENT_BALANCE, is_tracking=False)
        last_quote = self.START_VALUE * 0.5
        self.system.update_start_stop_values_if_necessary(last_quote)
        self.assertEqual(self.system.start_value, last_quote)
        self.assertEqual(self.system.stop_value, self.STOP_VALUE * 0.5)

        self.system.start_value = self.START_VALUE
        self.system.stop_value = self.STOP_VALUE

        last_quote = self.STOP_VALUE * 2
        self.system.update_start_stop_values_if_necessary(last_quote)
        self.assertEqual(self.system.start_value, self.START_VALUE * 2)
        self.assertEqual(self.system.stop_value, last_quote)

        self.system.start_value = self.START_VALUE
        self.system.stop_value = self.STOP_VALUE
        last_quote = (self.START_VALUE + self.STOP_VALUE) / 2
        self.system.update_start_stop_values_if_necessary(last_quote)
        self.assertEqual(self.system.start_value, self.START_VALUE)
        self.assertEqual(self.system.stop_value, self.STOP_VALUE)

    def test_it_stop_loss_when_not_tracking(self):
        self._set_up_for_selling_purposes(
            self.START_VALUE * ((100.0 - self.STOP_LOSS_TRIGGER) / 100) - 0.01, self.CURRENT_BALANCE, is_tracking=False
        )
        self.system.run()
        self._assert_results(buy_call_count=0, sell_call_count=1, order_side=consts.OrderSide.BUY, is_tracking=False)
