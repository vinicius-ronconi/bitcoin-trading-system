from unittest import TestCase
import mock
from trading_system.api import beans, consts
from trading_system.systems.trailing_orders import TrailingOrders


class TrailingOrdersTestCase(TestCase):
    def setUp(self):
        self.get_start_value_method = mock.MagicMock(return_value=2000)
        start_value_patcher = mock.patch(
            'trading_system.systems.trailing_orders.TrailingOrders._get_start_value', self.get_start_value_method
        )
        self.addCleanup(start_value_patcher.stop)
        start_value_patcher.start()

        self.get_stop_value_method = mock.MagicMock(return_value=2500)
        stop_value_patcher = mock.patch(
            'trading_system.systems.trailing_orders.TrailingOrders._get_stop_value', self.get_stop_value_method
        )
        self.addCleanup(stop_value_patcher.stop)
        stop_value_patcher.start()

        self.get_order_placement_perc_method = mock.MagicMock(return_value=1)
        order_placement_perc_patcher = mock.patch(
            'trading_system.systems.trailing_orders.TrailingOrders._get_order_placement_percentage',
            self.get_order_placement_perc_method
        )
        self.addCleanup(order_placement_perc_patcher.stop)
        order_placement_perc_patcher.start()

        self.stop_loss_trigger_method = mock.MagicMock(return_value=2)
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
            last_value=1900,
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

        self.system.run()
