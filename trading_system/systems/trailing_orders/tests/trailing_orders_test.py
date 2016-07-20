from unittest import TestCase

import mock

from trading_system import consts
from trading_system.api.interfaces import IClient
from trading_system.systems.trailing_orders import TrailingOrders


class TrailingOrdersTestCase(TestCase):
    START_VALUE = 100.0
    STOP_VALUE = 200.0

    @mock.patch('trading_system.systems.trailing_orders.TrailingOrders._get_start_value', return_value=START_VALUE)
    @mock.patch('trading_system.systems.trailing_orders.TrailingOrders._get_stop_value', return_value=STOP_VALUE)
    @mock.patch(
        'trading_system.systems.trailing_orders.TrailingOrders._get_order_placement_percentage', return_value=5.0
    )
    @mock.patch('trading_system.systems.trailing_orders.TrailingOrders._get_stop_loss_trigger', return_value=5.0)
    @mock.patch('trading_system.systems.trailing_orders.TrailingOrders._get_next_operation', return_value=1)
    def setUp(self, start_value, stop_value, order_perc, stop_loss_trigger, next_operation):
        client = mock.Mock(IClient)
        self.system = TrailingOrders(client)

    def test_it_update_start_stop_values_if_necessary(self):
        last_quote = self.START_VALUE / 2
        self.system.update_start_stop_values_if_necessary(last_quote)
        self.assertEqual(self.system.start_value, last_quote)
        self.assertEqual(self.system.stop_value, self.STOP_VALUE * (last_quote/self.START_VALUE))

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

    @mock.patch('trading_system.systems.trailing_orders.commands.BuyBitcoinsCommand.execute')
    def test_it_calls_buy_command(self, command):
        self.system.next_operation = consts.OrderSide.BUY
        self.system.client.orders.get_pending_orders.return_value = [None]
        self.system.update_start_stop_values_if_necessary = mock.Mock()
        self.system.run()
        self.assertEqual(command.call_count, 1)

    @mock.patch('trading_system.systems.trailing_orders.commands.SellBitcoinsCommand.execute')
    def test_it_calls_sell_command(self, command):
        self.system.next_operation = consts.OrderSide.SELL
        self.system.client.orders.get_pending_orders.return_value = [None]
        self.system.update_start_stop_values_if_necessary = mock.Mock()
        self.system.run()
        self.assertEqual(command.call_count, 1)

    @mock.patch('trading_system.systems.trailing_orders.commands.EvaluatePendingOrdersCommand.execute')
    def test_it_calls_sell_command(self, command):
        self.system.next_operation = consts.OrderSide.SELL
        self.system.client.orders.get_pending_orders.return_value = 'any_fake_content'
        self.system.update_start_stop_values_if_necessary = mock.Mock()
        self.system.run()
        self.assertEqual(command.call_count, 1)

        self.system.next_operation = consts.OrderSide.SELL
        self.system.run()
        self.assertEqual(command.call_count, 2)

    def test_it_gets_buy_price(self):
        self.system.start_value = 100.0
        self.system.order_placement_perc = 5.0
        self.assertEqual(self.system.buy_price, 105.0)

    def test_it_gets_sell_price(self):
        self.system.stop_value = 100.0
        self.system.order_placement_perc = 5.0
        self.assertEqual(self.system.sell_price, 95.0)

    def test_it_gets_stop_loss_price(self):
        self.system.start_value = 100.0
        self.system.stop_loss_trigger = 5.0
        self.assertEqual(self.system.stop_loss_price, 95.0)
