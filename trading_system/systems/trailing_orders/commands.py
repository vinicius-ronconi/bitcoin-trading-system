from trading_system import consts, utils
from trading_system.systems.interfaces import IOrderCommand


class BuyBitcoinsCommand(IOrderCommand):
    def __init__(self, system):
        """
        :type system: trading_system.systems.trailing_orders.TrailingOrders
        """
        self.system = system

    def execute(self, last_quote):
        """
        :type last_quote: float
        """
        evaluate_func = self._get_buy_operation_func()
        evaluate_func(last_quote)

    def _get_buy_operation_func(self):
        return {
            True: self._evaluate_last_quote_to_buy_bitcoins,
            False: self._evaluate_last_quote_to_start_buying_track,
        }[self.system.is_tracking]

    def _evaluate_last_quote_to_buy_bitcoins(self, last_quote):
        if last_quote >= self.system.buy_price:
            quantity = utils.get_floor_in_satoshi_precision(self.system.balance.currency / last_quote)
            self.system.log_info(
                'BUYING {quantity} BITCOINS - price: {value}'.format(quantity=quantity, value=self.system.buy_price)
            )
            self.system.client.orders.buy_bitcoins_with_limited_order(self.system.buy_price, quantity)
            self.system.set_next_operation(consts.OrderSide.SELL)
            self.system.is_tracking = False

    def _evaluate_last_quote_to_start_buying_track(self, last_quote):
        self.system.is_tracking = (last_quote <= self.system.setup.start_value)
        if self.system.is_tracking:
            self.system.log_info(
                'Tracking values to place a BUY order after quote become lower than {start}. '
                'Last quote was {last} and will but an order after price become higher than {buy_price}'.format(
                    start=self.system.setup.start_value, last=last_quote, buy_price=self.system.buy_price,
                )
            )


class SellBitcoinsCommand(IOrderCommand):
    def __init__(self, system):
        """
        :type system: trading_system.systems.trailing_orders.TrailingOrders
        """
        self.system = system

    def execute(self, last_quote):
        """
        :type last_quote: float
        """
        evaluate_func = self._get_sell_operation_func(last_quote)
        evaluate_func(last_quote)

    def _get_sell_operation_func(self, last_quote):
        if last_quote < self.system.stop_loss_price:
            return self._evaluate_stop_loss

        return {
            True: self._evaluate_last_quote_to_sell_bitcoins,
            False: self._evaluate_last_quote_to_start_selling_track,
        }[self.system.is_tracking]

    def _evaluate_last_quote_to_sell_bitcoins(self, last_quote):
        if last_quote <= self.system.sell_price:
            self.system.log_info('SELLING {quantity} BITCOINS - price: {value}'.format(
                quantity=self.system.balance.btc, value=self.system.sell_price)
            )
            self._sell_bitcoins(self.system.sell_price)
            self.system.is_tracking = False

    def _sell_bitcoins(self, sell_value):
        self.system.client.orders.sell_bitcoins_with_limited_order(sell_value, self.system.balance.btc)
        self.system.set_next_operation(consts.OrderSide.BUY)

    def _evaluate_last_quote_to_start_selling_track(self, last_quote):
        self.system.is_tracking = last_quote >= self.system.setup.stop_value
        if self.system.is_tracking:
            self.system.log_info(
                'Tracking values to place a SELL order after quote become lower than {stop}. '
                'Last quote was {last} and will but an order after price become lower than {sell_price}'.format(
                    stop=self.system.setup.stop_value, last=last_quote, sell_price=self.system.sell_price)

            )

    def _evaluate_stop_loss(self, last_quote):
        if last_quote <= self.system.stop_loss_price:
            self.system.log_info('STOPPING LOSS {quantity} BITCOINS - price: {value}'.format(
                quantity=self.system.balance.btc, value=self.system.stop_loss_price)
            )
            self._sell_bitcoins(self.system.stop_loss_price)
            self.system.is_tracking = True


class EvaluatePendingOrdersCommand(IOrderCommand):
    def __init__(self, system):
        """
        :type system: trading_system.systems.trailing_orders.TrailingOrders
        """
        self.system = system

    def execute(self, last_quote):
        """
        :type last_quote: float
        """
        # TODO Check if should cancel order
        # Cancel buying order if last_quote > order price * order_placement_perc
        # Cancel selling order if last_quote < order price * order_placement_perc
        pass
