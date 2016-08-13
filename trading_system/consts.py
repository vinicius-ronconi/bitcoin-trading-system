class Environment:
    PRODUCTION = 'prod'
    TEST = 'test'

ENVIRONMENTS_CHOICES = {Environment.PRODUCTION, Environment.TEST}


class Currency:
    AMERICAN_DOLLAR = 'USD'
    BRAZILIAN_REAIS = 'BRL'
    CHILEAN_PESOS = 'CLP'
    PAKISTANI_RUPEE = 'PKR'
    VENEZUELAN_BOLIVARES = 'VEF'
    VIETNAMESE_DONGS = 'VND'


class Symbol:
    BTCUSD = 'BTCUSD'
    BTCBRL = 'BTCBRL'
    BTCCLP = 'BTCCLP'
    BTCPKR = 'BTCPKR'
    BTCVEF = 'BTCVEF'
    BTCVND = 'BTCVND'

CURRENCY_TO_SYMBOL_MAP = {
    Currency.AMERICAN_DOLLAR: Symbol.BTCUSD,
    Currency.BRAZILIAN_REAIS: Symbol.BTCBRL,
    Currency.CHILEAN_PESOS: Symbol.BTCCLP,
    Currency.PAKISTANI_RUPEE: Symbol.BTCPKR,
    Currency.VENEZUELAN_BOLIVARES: Symbol.BTCVEF,
    Currency.VIETNAMESE_DONGS: Symbol.BTCVND,
}


class Broker:
    SURBITCOIN = '1'
    VBTC = '3'
    FOXBIT = '4'
    TESTNET = '5'
    URDUBIT = '8'
    CHILEBIT = '9'


class OrderSide:
    BUY = '1'
    SELL = '2'

ORDER_SIDE_TO_TEXT_MAP = {
    OrderSide.BUY: 'buy',
    OrderSide.SELL: 'sell',
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
