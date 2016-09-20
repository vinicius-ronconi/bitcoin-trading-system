from unittest import TestCase

import mock

from trading_system import consts
from trading_system.api.beans import PlacedOrder, Ticker
from trading_system.systems.trailing_orders.system import TrailingOrders
from trading_system.systems.trailing_orders import beans, factory, states


class TrailingOrdersTestCase(TestCase):
    START_VALUE = 100.0
    STOP_VALUE = 200.0
    REVERSAL = 5
    STOP_LOSS = 20
    OPERATIONAL_COST = 1
    PROFIT = 2

    INITIAL_SETUP = beans.TrailingOrderSetup(
        next_operation=consts.OrderSide.BUY,
        start_value=START_VALUE,
        stop_value=STOP_VALUE,
        reversal=REVERSAL,
        stop_loss=STOP_LOSS,
        operational_cost=OPERATIONAL_COST,
        profit=PROFIT,
    )

    def setUp(self):
        client = mock.MagicMock()
        bootstrap = factory.TrailingOrdersFactory().make_fake_bootstrap(
            beans.TrailingOrderSetup(
                next_operation=consts.OrderSide.SELL,
                start_value=100,
                stop_value=200,
                reversal=10,
                stop_loss=20,
                operational_cost=1,
                profit=2,
            )
        )

        logging_patch = mock.patch('trading_system.systems.trailing_orders.system.logging')
        self.addCleanup(logging_patch.stop)
        logging_patch.start()

        self.system = TrailingOrders(client, bootstrap)
        self.system.get_pending_orders = mock.MagicMock(return_value=[])

        self.set_next_operation = mock.MagicMock()
        next_operation_patcher = mock.patch(
            'trading_system.systems.trailing_orders.system.TrailingOrders.set_next_operation', self.set_next_operation
        )
        self.addCleanup(next_operation_patcher.stop)
        next_operation_patcher.start()

    def test_it_places_a_sell_order(self):
        self.system.set_state(states.TrackingToSellState(self.system))
        self._set_last_quote(self.system.sell_price)
        self.system.run()
        self._assert_results(
            sell_limited_call_count=1, sell_market_call_count=0, expected_state=states.PendingToSellState
        )

        self.system.set_state(states.TrackingToSellState(self.system))
        self._set_last_quote(self.system.sell_price - 0.01)
        self.system.run()
        self._assert_results(
            sell_limited_call_count=2, sell_market_call_count=0, expected_state=states.PendingToSellState
        )

    def test_it_does_not_place_a_sell_order_besides_is_tracking(self):
        self.system.set_state(states.TrackingToSellState(self.system))
        self._set_last_quote(self.system.sell_price + 0.01)
        self.system.run()
        self._assert_results(
            sell_limited_call_count=0, sell_market_call_count=0, expected_state=states.TrackingToSellState
        )

    def test_it_starts_tracking(self):
        self.system.set_state(states.WaitingToSellState(self.system))
        self._set_last_quote(self.system.setup.stop_value)
        self.system.run()
        self._assert_results(
            sell_limited_call_count=0, sell_market_call_count=0, expected_state=states.TrackingToSellState
        )

        self.system.set_state(states.WaitingToSellState(self.system))
        self._set_last_quote(self.system.setup.stop_value + 0.01)
        self.system.run()
        self._assert_results(
            sell_limited_call_count=0, sell_market_call_count=0, expected_state=states.TrackingToSellState
        )

        self.system.set_state(states.WaitingToSellState(self.system))
        last_quote = self.system.setup.stop_value * 2
        self._set_last_quote(last_quote)
        self.system.run()
        self._assert_results(
            sell_limited_call_count=0, sell_market_call_count=0, expected_state=states.TrackingToSellState
        )
        self.assertEqual(self.system.setup.start_value, self.START_VALUE * 2)
        self.assertEqual(self.system.setup.stop_value, last_quote)

    def test_it_does_not_start_tracking_for_selling_purposes(self):
        self.system.set_state(states.WaitingToSellState(self.system))
        self._set_last_quote(self.system.setup.stop_value - 0.01)
        self.system.run()
        self._assert_results(
            sell_limited_call_count=0, sell_market_call_count=0, expected_state=states.WaitingToSellState
        )

    def test_it_stops_loss(self):
        self.system.set_state(states.WaitingToSellState(self.system))
        self._set_last_quote(self.system.stop_loss_price - 0.01)
        self.system.run()
        self._assert_results(
            sell_limited_call_count=0, sell_market_call_count=1, expected_state=states.PendingToSellState
        )

        self.system.set_state(states.TrackingToSellState(self.system))
        self._set_last_quote(self.system.stop_loss_price - 0.01)
        self.system.run()
        self._assert_results(
            sell_limited_call_count=0, sell_market_call_count=2, expected_state=states.PendingToSellState
        )

        self.system.set_state(states.PendingToSellState(self.system, states.WaitingToBuyState(self.system)))
        self.system.get_pending_orders.return_value = [
            PlacedOrder(
                order_id='my_order_id',
                exec_id='my_exec_id',
                exec_type='exec_type',
                order_status='order_status',
                price=100.0,
                symbol='BTCUSD',
                amount=1.0,
                message_type=None,
                order_rejection_reason=None,
                side='sell',
                client_order_id='my_order_id'
            )
        ]
        self._set_last_quote(self.system.stop_loss_price - 0.01)
        self.system.run()
        self._assert_results(
            sell_limited_call_count=0, sell_market_call_count=3, expected_state=states.PendingToSellState
        )

    def test_it_does_not_stop_loss_when_not_needed(self):
        self.system.set_state(states.WaitingToSellState(self.system))
        self._set_last_quote(self.system.stop_loss_price)
        self.system.run()
        self._assert_results(
            sell_limited_call_count=0, sell_market_call_count=0, expected_state=states.WaitingToSellState
        )

        self.system.set_state(states.WaitingToSellState(self.system))
        self._set_last_quote(self.system.stop_loss_price + 0.01)
        self.system.run()
        self._assert_results(
            sell_limited_call_count=0, sell_market_call_count=0, expected_state=states.WaitingToSellState
        )

    def test_it_goes_to_buying_mode(self):
        self.system.set_state(states.PendingToSellState(self.system, states.WaitingToBuyState(self.system)))
        self.system.get_pending_orders.return_value = []
        self.system.run()
        self._assert_results(
            sell_limited_call_count=0, sell_market_call_count=0, expected_state=states.WaitingToBuyState
        )

        self.system.set_state(states.PendingToSellState(self.system, states.TrackingToBuyState(self.system)))
        self.system.get_pending_orders.return_value = []
        self.system.run()
        self._assert_results(
            sell_limited_call_count=0, sell_market_call_count=0, expected_state=states.TrackingToBuyState
        )

    def _set_last_quote(self, last_quote):
        self.system.get_current_ticker = mock.MagicMock(return_value=Ticker(
            currency_pair='BTCUSD',
            last_value=last_quote,
            highest_value=200.0,
            lowest_value=100.0,
            best_sell_order=140.0,
            best_buy_order=120.0,
            volume_btc=100,
            volume_currency=100,
        ))

    def _assert_results(self, sell_limited_call_count, sell_market_call_count, expected_state):
        self.assertEqual(self.system.client.orders.buy_bitcoins_with_limited_order.call_count, 0)
        self.assertEqual(self.system.client.orders.sell_bitcoins_with_limited_order.call_count, sell_limited_call_count)
        self.assertEqual(self.system.client.orders.sell_bitcoins_with_market_order.call_count, sell_market_call_count)
        self.assertIsInstance(self.system.state, expected_state)
