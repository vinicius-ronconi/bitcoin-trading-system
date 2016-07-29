NONCE_PRECISION = 1000000  # 6 decimal digits
SATOSHI_PRECISION = 100000000  # 8 decimal digits


class Environment:
    PRODUCTION = 'prod'
    TEST = 'test'

ENVIRONMENTS_CHOICES = {Environment.PRODUCTION, Environment.TEST}


class Currency:
    AMERICAN_DOLAR = 'USD'
    BRAZILIAN_REAIS = 'BRL'
    CHILEAN_PESOS = 'CLP'
    PAKISTANI_RUPPE = 'PKR'
    VENEZUELAN_BOLIVARES = 'VEF'
    VIETNAMISE_DONGS = 'VND'

CURRENCIES_CHOICES = {
    Currency.BRAZILIAN_REAIS,
    Currency.CHILEAN_PESOS,
    Currency.PAKISTANI_RUPPE,
    Currency.VENEZUELAN_BOLIVARES,
    Currency.VIETNAMISE_DONGS,
}


class Broker:
    SURBITCOIN = '1'
    VBTC = '3'
    FOXBIT = '4'
    TESTNET = '5'
    URDUBIT = '8'
    CHILEBIT = '9'

BROKERS_CHOICES = {
    Broker.SURBITCOIN,
    Broker.VBTC,
    Broker.FOXBIT,
    Broker.TESTNET,
    Broker.URDUBIT,
    Broker.CHILEBIT,
}


class MarketInformation:
    TICKER = 'ticker'
    ORDER_BOOK = 'orderbook'
    TRADES = 'trades'

MARKET_DATA_TYPE_CHOICES = {MarketInformation.TICKER, MarketInformation.ORDER_BOOK, MarketInformation.TRADES}


class OrderSide:
    BUY = '1'
    SELL = '2'

ORDER_SIDE_TO_TEXT_MAP = {
    OrderSide.BUY: 'buy',
    OrderSide.SELL: 'sell',
}

ORDER_SIDE_CHOICES = {OrderSide.BUY, OrderSide.SELL}


class OrderType:
    MARKET = '1'
    LIMITED_ORDER = '2'

ORDER_TYPE_CHOICES = {OrderType.MARKET, OrderType.LIMITED_ORDER}


class MessageType:
    BALANCE = 'U2'
    BALANCE_RESPONSE = 'U3'
    CANCEL_ORDER = 'F'
    GET_ORDERS = 'U4'
    POSITION = 'U42'
    PLACE_ORDER = 'D'
    PLACE_ORDER_RESPONSE = '8'
    ORDER_STATUS_RESPONSE = 'U5'
    TRADE_HISTORY = 'U32'
    TRADERS_RANK = 'U36'

MESSAGE_TYPE_CHOICES = {
    MessageType.BALANCE,
    MessageType.CANCEL_ORDER,
    MessageType.GET_ORDERS,
    MessageType.POSITION,
    MessageType.PLACE_ORDER,
    MessageType.TRADE_HISTORY,
    MessageType.TRADERS_RANK,
}


class OrderStatus:
    NEW = '0'
    PARTIALLY_FILL = '1'
    FILL = '2'
    CANCELLED = '4'
    REJECTED = '8'
    PENDING_NEW = 'A'

ORDER_STATUS_CHOICES = {
    OrderStatus.NEW,
    OrderStatus.PARTIALLY_FILL,
    OrderStatus.FILL,
    OrderStatus.CANCELLED,
    OrderStatus.REJECTED,
    OrderStatus.PENDING_NEW,
}


class OrderRejectedReason:
    VALUE_TOO_SMALL = '3'

ORDER_REJECTED_REASON_CHOICES = {
    OrderRejectedReason.VALUE_TOO_SMALL
}


class Symbol:
    BTCUSD = 'BTCUSD'
    BTCBRL = 'BTCBRL'
    BTCCLP = 'BTCCLP'
    BTCPKR = 'BTCPKR'
    BTCVEF = 'BTCVEF'
    BTCVND = 'BTCVND'

CURRENCY_TO_SYMBOL_MAP = {
    Currency.AMERICAN_DOLAR: Symbol.BTCUSD,
    Currency.BRAZILIAN_REAIS: Symbol.BTCBRL,
    Currency.CHILEAN_PESOS: Symbol.BTCCLP,
    Currency.PAKISTANI_RUPPE: Symbol.BTCPKR,
    Currency.VENEZUELAN_BOLIVARES: Symbol.BTCVEF,
    Currency.VIETNAMISE_DONGS: Symbol.BTCVND,
}
