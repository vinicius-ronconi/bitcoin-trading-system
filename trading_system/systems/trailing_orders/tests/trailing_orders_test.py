from unittest import TestCase

import mock

from trading_system import consts
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

    def test_it_gets_buy_price(self):
        self._setup_operation(consts.OrderSide.BUY)
        self.assertEqual(self.system.buy_price, 105.0)

    def test_it_gets_sell_price(self):
        self._setup_operation(consts.OrderSide.SELL)
        self.assertEqual(self.system.sell_price, 190.0)

    def test_it_gets_stop_loss_price(self):
        self._setup_operation(consts.OrderSide.SELL)
        self.assertEqual(self.system.stop_loss_price, 90.0)

    def test_it_sets_next_operation(self):
        self._setup_operation(consts.OrderSide.BUY)
        self.system.set_next_operation(consts.OrderSide.SELL)
        self.assertEqual(self.system.setup.next_operation, consts.OrderSide.SELL)

        self.system.set_next_operation(consts.OrderSide.BUY)
        self.assertEqual(self.system.setup.next_operation, consts.OrderSide.BUY)

    def _setup_operation(self, next_operation):
        client = mock.Mock()
        bootstrap = TrailingOrdersFactory().make_fake_bootstrap(
            TrailingOrderSetup(
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
