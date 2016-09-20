from trading_system import consts
from trading_system.systems.trailing_orders.beans import TrailingOrderSetup
from trading_system.systems.trailing_orders.interfaces import ISystemState
from trading_system.utils import get_floor_in_satoshi_precision, get_rounded_decimal_value


class WaitingToBuyState(ISystemState):
    def __init__(self, system):
        """
        :type system: trading_system.systems.trailing_orders.interfaces.ITrailingOrdersSystem
        """
        self.system = system
        self.system.is_tracking = False
        self.system.set_next_operation(consts.OrderSide.BUY)

    def evaluate_last_quote(self, last_quote):
        if last_quote <= self.system.setup.start_value:
            self._start_tracking(last_quote)
        elif last_quote > self.system.setup.stop_value:
            self._update_setup_when_last_quote_higher_than_stop_value(last_quote)
        elif self.system.setup.start_value < self.system.current_ticker.lowest_value:
            self._update_setup_when_start_value_lower_than_24_hours_minimum()

    def _start_tracking(self, last_quote):
        update_system_setup(self.system, update_factor=last_quote / self.system.setup.start_value)
        self.system.set_state(TrackingToBuyState(self.system))
        self.system.log_info(
            'Tracking values to place a BUY order after quote become lower than {start}. '
            'Last quote was {last} and will but an order after price become higher than {buy_price}'.format(
                start=self.system.setup.start_value, last=last_quote, buy_price=self.system.buy_price,
            )
        )

    def _update_setup_when_last_quote_higher_than_stop_value(self, last_quote):
        update_system_setup(self.system, update_factor=last_quote / self.system.setup.stop_value)
        self.system.log_info(
            'Updating setup because last quote ({}) > stop value ({}).'.format(last_quote, self.system.setup.stop_value)
        )
        self.system.print_current_values()

    def _update_setup_when_start_value_lower_than_24_hours_minimum(self):
        update_system_setup(
            self.system, update_factor=self.system.current_ticker.lowest_value / self.system.setup.start_value
        )
        self.system.log_info(
            'Updating setup because start value ({}) < lowest quote in 24hrs ({}).'.format(
                self.system.setup.start_value, self.system.current_ticker.lowest_value
            )
        )
        self.system.print_current_values()


class TrackingToBuyState(ISystemState):
    def __init__(self, system):
        """
        :type system: trading_system.systems.trailing_orders.interfaces.ITrailingOrdersSystem
        """
        self.system = system
        self.system.is_tracking = True
        self.system.set_next_operation(consts.OrderSide.BUY)

    def evaluate_last_quote(self, last_quote):
        if last_quote < self.system.setup.start_value:
            self._update_setup(last_quote)
        elif last_quote >= self.system.buy_price:
            self._buy_bitcoins(last_quote)

    def _update_setup(self, last_quote):
        update_system_setup(self.system, update_factor=last_quote / self.system.setup.start_value)
        self.system.log_info(
            'Updating setup because last quote ({}) < start value ({}).'.format(
                last_quote, self.system.setup.start_value
            )
        )
        self.system.print_current_values()

    def _buy_bitcoins(self, last_quote):
        quantity = get_floor_in_satoshi_precision(self.system.balance.currency / last_quote)
        self.system.log_info(
            'BUYING {quantity} BITCOINS - price: {value} after last_quote = {last_quote}'.format(
                quantity=quantity, value=self.system.buy_price, last_quote=last_quote
            )
        )
        self.system.client.orders.buy_bitcoins_with_limited_order(self.system.buy_price, quantity)
        self.system.set_state(PendingToBuyState(self.system))


class PendingToBuyState(ISystemState):
    def __init__(self, system):
        """
        :type system: trading_system.systems.trailing_orders.interfaces.ITrailingOrdersSystem
        """
        self.system = system
        self.system.is_tracking = False

    def evaluate_last_quote(self, last_quote):
        pending_orders = self.system.get_pending_orders()
        cancel_price = self.system.buy_price * (1.0 + self.system.setup.profit)
        if not pending_orders:
            self._change_state_to_waiting_to_sell()
        elif last_quote > cancel_price:
            self._cancel_order(pending_orders[0].order_id, last_quote, cancel_price)

    def _change_state_to_waiting_to_sell(self):
        self.system.set_state(WaitingToSellState(self.system))
        self.system.log_info('No pending order found. It looks like the bitcoins were bought.')

    def _cancel_order(self, order_id, last_quote, cancel_price):
        self.system.client.orders.cancel_order(order_id)
        self.system.set_state(WaitingToBuyState(self.system))
        self.system.log_info(
            'Cancelling the buy order. last quote ({}) > cancel price ({})'.format(last_quote, cancel_price)
        )


class WaitingToSellState(ISystemState):
    def __init__(self, system):
        """
        :type system: trading_system.systems.trailing_orders.interfaces.ITrailingOrdersSystem
        """
        self.system = system
        self.system.is_tracking = False
        self.system.set_next_operation(consts.OrderSide.SELL)

    def evaluate_last_quote(self, last_quote):
        if last_quote >= self.system.setup.stop_value:
            self._start_tracking(last_quote)
        elif last_quote < self.system.stop_loss_price:
            stop_loss(self.system, last_quote)

    def _start_tracking(self, last_quote):
        update_system_setup(self.system, update_factor=last_quote / self.system.setup.stop_value)
        self.system.set_state(TrackingToSellState(self.system))
        self.system.log_info(
            'Tracking values to place a SELL order after quote become lower than {stop}. '
            'Last quote was {last} and will but an order after price become lower than {sell_price}'.format(
                stop=self.system.setup.stop_value, last=last_quote, sell_price=self.system.sell_price)

        )
        self.system.print_current_values()


class TrackingToSellState(ISystemState):
    def __init__(self, system):
        """
        :type system: trading_system.systems.trailing_orders.interfaces.ITrailingOrdersSystem
        """
        self.system = system
        self.system.is_tracking = True
        self.system.set_next_operation(consts.OrderSide.SELL)

    def evaluate_last_quote(self, last_quote):
        if last_quote > self.system.setup.stop_value:
            self._update_setup_when_last_quote_was_higher_than_stop_value(last_quote)
        elif last_quote < self.system.stop_loss_price:
            stop_loss(self.system, last_quote)
        elif last_quote <= self.system.sell_price:
            self._sell_bitcoins(last_quote)

    def _update_setup_when_last_quote_was_higher_than_stop_value(self, last_quote):
        update_system_setup(self.system, update_factor=last_quote / self.system.setup.stop_value)
        self.system.log_info(
            'Updating setup because last quote ({}) > stop value ({}).'.format(
                last_quote, self.system.setup.stop_value
            )
        )
        self.system.print_current_values()

    def _sell_bitcoins(self, last_quote):
        self.system.client.orders.sell_bitcoins_with_limited_order(self.system.sell_price, self.system.balance.btc)
        self.system.log_info('SELLING {quantity} BITCOINS - price: {value} after last quote = {last_quote}'.format(
            quantity=self.system.balance.btc, value=self.system.sell_price, last_quote=last_quote)
        )
        self.system.set_state(PendingToSellState(self.system, WaitingToBuyState(self.system)))


class PendingToSellState(ISystemState):
    def __init__(self, system, next_state):
        """
        :type system: trading_system.systems.trailing_orders.interfaces.ITrailingOrdersSystem
        :type next_state: trading_system.systems.trailing_orders.interfaces.ISystemState
        """
        self.system = system
        self.next_state = next_state
        self.system.is_tracking = False

    # If last_quote < stop_loss_price -> update values, Cancel Current Order,
    #   Place MARKET Order and Change State to PendingToSellState
    # If no pending order was found -> Change State to WaitingToBuyState
    def evaluate_last_quote(self, last_quote):
        pending_orders = self.system.get_pending_orders()
        if not pending_orders:
            self._change_to_buy_state()
        elif last_quote < self.system.stop_loss_price:
            self._stop_loss(pending_orders[0].order_id, last_quote)

    def _change_to_buy_state(self):
        self.system.set_state(self.next_state)
        self.system.log_info('No pending order found. It looks like the bitcoins were sold.')

    def _stop_loss(self, order_id, last_quote):
        self._cancel_order(order_id, last_quote)
        self.system.update_balance()
        stop_loss(self.system, last_quote)

    def _cancel_order(self, order_id, last_quote):
        self.system.client.orders.cancel_order(order_id)
        self.system.set_state(WaitingToBuyState(self.system))
        self.system.log_info(
            'Cancelling the sell order. last quote ({}) < stop loss ({})'.format(
                last_quote, self.system.stop_loss_price
            )
        )


def update_system_setup(system, update_factor):
    """
    :type system: trading_system.systems.trailing_orders.interfaces.ITrailingOrdersSystem
    :type update_factor: float
    """
    system.update_setup(
        TrailingOrderSetup(
            next_operation=system.setup.next_operation,
            start_value=get_rounded_decimal_value(system.setup.start_value * update_factor),
            stop_value=get_rounded_decimal_value(system.setup.stop_value * update_factor),
            reversal=system.setup.reversal,
            stop_loss=system.setup.stop_loss,
            operational_cost=system.setup.operational_cost,
            profit=system.setup.profit,
        )
    )


def stop_loss(system, last_quote):
    system.client.orders.sell_bitcoins_with_market_order(system.balance.btc)
    update_system_setup(system, update_factor=last_quote / system.setup.start_value)
    system.set_state(PendingToSellState(system, TrackingToBuyState(system)))
    system.log_info(
        'STOP LOSS because last quote ({}) < stop loss price ({}).'.format(
            last_quote, system.stop_loss_price
        )
    )
    system.print_current_values()
