from trading_system.systems.trailing_orders.interfaces import ISystemState


class WaitingToBuyState(ISystemState):
    # If last_quote <= start_price -> update values and Change State to TrackingToBuyState
    # If last_quote > stop_price -> update_values
    def evaluate_last_quote(self, last_quote):
        super().evaluate_last_quote(last_quote)


class TrackingToBuyState(ISystemState):
    # If last_quote < start_price -> update values
    # If last_quote >= buy_price -> Place Order and Change State to PendingToBuyState
    def evaluate_last_quote(self, last_quote):
        super().evaluate_last_quote(last_quote)


class PendingToBuyState(ISystemState):
    # If last_quote > buy_price + reversal trend % -> Cancel Order and Change State to WaitingToBuyState
    # If no pending order was found -> Change State to WaitingToSellState
    def evaluate_last_quote(self, last_quote):
        super().evaluate_last_quote(last_quote)


class WaitingToSellState(ISystemState):
    # If last_quote >= stop_price -> update values and Change State to TrackingToSellState
    # If last_quote < stop_loss_price -> update values, Place MARKET Order and Change State to PendingToSellState
    def evaluate_last_quote(self, last_quote):
        super().evaluate_last_quote(last_quote)


class TrackingToSellState(ISystemState):
    # If last_quote > stop_value -> update values
    # If last_quote < stop_loss_price -> update values, Place MARKET Order and Change State to PendingToSellState
    # If last_quote < sell_value -> Place Order and Change State to PendingToSellState
    def evaluate_last_quote(self, last_quote):
        super().evaluate_last_quote(last_quote)


class PendingToSellState(ISystemState):
    # If last_quote < stop_loss_price -> update values, Cancel Current Order, Place MARKET Order and Change State to PendingToSellState
    # If no pending order was found -> Change State to WaitingToBuyState
    def evaluate_last_quote(self, last_quote):
        super().evaluate_last_quote(last_quote)
