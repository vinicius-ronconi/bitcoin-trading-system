from unittest import TestCase
import mock
from trading_system.api import beans, consts
from trading_system.systems.trailing_orders import TrailingOrders


class TrailingOrdersTestCase(TestCase):
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
        get_ticker = mock.MagicMock(return_value=beans.Ticker(
            currency_pair='BTCBRL',
            last_value=round(self.START_VALUE * ((100 + self.ORDER_PLACEMENT_PERC) / 100), 2),
            highest_value=2300,
            lowest_value=2200,
            best_sell_order=2205,
            best_buy_order=2195,
            volume_btc=200,
            volume_currency=400000,
        ))
        ticker_patcher = mock.patch('trading_system.api.markets.BlinkTradeMarketApi.get_ticker', get_ticker)
        self.addCleanup(ticker_patcher.stop)
        ticker_patcher.start()

        self.system.is_tracking = True

        self.system.client = mock.Mock()
        self.system.run()

        self.assertEqual(self.system.client.orders.buy_bitcoins.call_count, 1)
        self.assertEqual(self.system.client.orders.sell_bitcoins.call_count, 0)
