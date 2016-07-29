from collections import namedtuple


class Balance(namedtuple('Balance', [
    'currency',  # float
    'currency_locked',  # float
    'btc',  # float
    'btc_locked',  # float
])):
    pass


class OrderInBook(namedtuple('Order', [
    'price',  # float
    'amount',  # float
    'user_id',  # int
])):
    pass


class OrderBook(namedtuple('OrderBook', [
    'currency_pair',  # str
    'bids',  # list[beans.OrderInBook]
    'asks',  # list[beans.OrderInBook]
])):
    pass


class PlacedOrder(namedtuple('PlacedOrder', [
    'order_id',  # [basestring|None]
    'exec_id',  # [basestring|None]
    'exec_type',  # [basestring|None]
    'order_status',  # basestring
    'price',  # float
    'symbol',  # basestring
    'amount',  # float
    'message_type',  # [basestring|None]
    'order_rejection_reason',  # [basestring|None]
    'side',  # basestring
    'client_order_id',  # basestring
])):
    pass


class Ticker(namedtuple('Ticker', [
    'currency_pair',  # str
    'last_value',  # float
    'highest_value',  # float
    'lowest_value',  # float
    'best_sell_order',  # float
    'best_buy_order',  # float
    'volume_btc',  # float
    'volume_currency',  # float
])):
    pass


class Trade(namedtuple('Trades', [
    'transaction_id',  # int
    'date',  # int
    'price',  # float
    'amount',  # float
    'side',  # str
])):
    pass
