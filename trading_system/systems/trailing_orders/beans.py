from collections import namedtuple
from trading_system.utils import get_rounded_decimal_value


class TrailingOrderSetup(namedtuple('TrailingOrderSetup', [
    'next_operation',  # basestring
    'start_value',  # float
    'stop_value',  # float
    'reversal',  # float
    'stop_loss',  # float
    'operational_cost',  # float
    'profit',  # float
])):
    @classmethod
    def make(cls, next_operation, start_value, stop_value, reversal, stop_loss, operational_cost, profit):
        return cls(
            next_operation=next_operation,
            start_value=get_rounded_decimal_value(start_value),
            stop_value=get_rounded_decimal_value(stop_value),
            reversal=get_rounded_decimal_value(reversal),
            stop_loss=get_rounded_decimal_value(stop_loss),
            operational_cost=get_rounded_decimal_value(operational_cost),
            profit=get_rounded_decimal_value(profit),
        )
