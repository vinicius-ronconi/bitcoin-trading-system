from collections import namedtuple


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
            start_value=start_value,
            stop_value=stop_value,
            reversal=reversal,
            stop_loss=stop_loss,
            operational_cost=operational_cost,
            profit=profit,
        )
