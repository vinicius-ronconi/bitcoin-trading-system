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
    pass
