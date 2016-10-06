from unittest import TestCase

import mock

from trading_system import consts
from trading_system.api.beans import PlacedOrder, Ticker
from trading_system.systems.trailing_orders.system import TrailingOrders
from trading_system.systems.trailing_orders.beans import TrailingOrderSetup
from trading_system.systems.trailing_orders.factory import TrailingOrdersFactory


class TrailingOrdersTestCase(TestCase):
    START_VALUE = 100.0
    STOP_VALUE = 200.0
    REVERSAL = 5
    STOP_LOSS = 10

    system_setup = NotImplemented
    system = NotImplemented

    def test_it_gets_buy_price(self):
        self._setup_operation(consts.OrderSide.BUY)
        self.assertEqual(self.system.buy_price, 105.0)

    def test_it_gets_sell_price(self):
        self._setup_operation(consts.OrderSide.SELL)
        self.assertEqual(self.system.sell_price, 190.0)

    def test_it_gets_stop_loss_price(self):
        self._setup_operation(consts.OrderSide.SELL)
        self.assertEqual(self.system.stop_loss_price, 90.0)

    def test_it_gets_pending_orders(self):
        self._setup_operation(consts.OrderSide.BUY)
        self.system.client.orders.get_pending_orders.return_value = [
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
                side='buy',
                client_order_id='my_order_id'
            )
        ]
        pending_orders = self.system.get_pending_orders()
        self.assertIsInstance(pending_orders, list)
        self.assertIsInstance(pending_orders[0], PlacedOrder)

    def test_it_gets_current_ticker(self):
        self._setup_operation(consts.OrderSide.BUY)
        self.system.client.market.get_ticker.return_value = Ticker(
            currency_pair='BTCBRL',
            last_value=100.0,
            highest_value=120.0,
            lowest_value=100.0,
            best_sell_order=110.0,
            best_buy_order=105.0,
            volume_btc=100.0,
            volume_currency=11000.0
        )
        ticker = self.system.get_current_ticker()
        self.assertIsInstance(ticker, Ticker)

    def _setup_operation(self, next_operation):
        client = mock.Mock()
        bootstrap = TrailingOrdersFactory().make_fake_bootstrap(
            TrailingOrderSetup.make(
                next_operation=next_operation,
                start_value=self.START_VALUE,
                stop_value=self.STOP_VALUE,
                reversal=self.REVERSAL,
                stop_loss=self.STOP_LOSS,
                operational_cost=0.2,
                profit=0.5,
            )
        )

        logging_patch = mock.patch('trading_system.systems.trailing_orders.system.logging')
        self.addCleanup(logging_patch.stop)
        logging_patch.start()

        self.system = TrailingOrders(client, bootstrap)
