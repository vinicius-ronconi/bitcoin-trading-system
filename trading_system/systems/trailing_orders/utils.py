from trading_system.utils import get_rounded_decimal_value


def get_buy_price(start_value, reversal):
    buy_price = start_value * ((100 + reversal) / 100)
    return get_rounded_decimal_value(buy_price)


def get_sell_price(stop_value, reversal):
    sell_price = stop_value * ((100.0 - reversal) / 100)
    return get_rounded_decimal_value(sell_price)


def get_stop_loss_price(start_value, stop_loss):
    stop_loss_price = start_value * ((100.0 - stop_loss) / 100)
    return get_rounded_decimal_value(stop_loss_price)
