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
    'order_id',  # int
    'time_in_force',  # basestring
    'exec_id',  # int
    'exec_type',  # basestring
    'order_status',  # basestring
    'cum_quantity',  # int
    'price',  # int
    'symbol',  # basestring
    'order_quantity',  # int
    'last_shares',  # int
    'last_px',  # int
    'cxl_quantity',  # int
    'volume',  # int
    'leaves_quantity',  # int
    'message_type',  # basestring
    'exec_side',  # basestring
    'order_type',  # basestring
    'order_rejection_reason',  # basestring
    'side',  # basestring
    'client_order_id',  # int
    'average_px',  # int
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
