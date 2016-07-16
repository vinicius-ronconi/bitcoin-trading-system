from trading_system.systems.interfaces import IOrderCommand
from trading_system.api import consts


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
            quantity = self.system.client.get_satoshi_value(self.system.balance.currency/last_quote)
            self.system.log_info(
                'BUYING {quantity} BITCOINS - price: {value}'.format(quantity=quantity, value=last_quote)
            )
            self.system.client.orders.buy_bitcoins(consts.OrderType.LIMITED_ORDER, last_quote, quantity)
            self.system.next_operation = consts.OrderSide.SELL
            self.system.is_tracking = False

    def _evaluate_last_quote_to_start_buying_track(self, last_quote):
        self.system.is_tracking = last_quote <= self.system.start_value
        if self.system.is_tracking:
            self.system.log_info('Tracking values to place a buy order')


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
                quantity=self.system.balance.btc, value=last_quote)
            )
            self._sell_bitcoins(last_quote)

    def _sell_bitcoins(self, sell_value):
        self.system.client.orders.sell_bitcoins(consts.OrderType.LIMITED_ORDER, sell_value, self.system.balance.btc)
        self.system.next_operation = consts.OrderSide.BUY
        self.system.is_tracking = False

    def _evaluate_last_quote_to_start_selling_track(self, last_quote):
        self.system.is_tracking = last_quote >= self.system.stop_value
        if self.system.is_tracking:
            self.system.log_info('Tracking values to place a sell order')

    def _evaluate_stop_loss(self, last_quote):
        if last_quote <= self.system.stop_loss_price:
            self.system.log_info('STOPPING LOSS {quantity} BITCOINS - price: {value}'.format(
                quantity=self.system.balance.btc, value=last_quote)
            )
            self._sell_bitcoins(last_quote)


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
