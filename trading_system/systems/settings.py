BITFINEX_KEY = 'my_api_key'
BITFINEX_SECRET = 'my_api_secret'

BLINKTRADE_KEY = 'my_api_key'
BLINKTRADE_SECRET = 'my_api_secret'

try:
    from . import settings_local
    BITFINEX_KEY = settings_local.BITFINEX_KEY
    BITFINEX_SECRET = settings_local.BITFINEX_SECRET

    BLINKTRADE_KEY = settings_local.BLINKTRADE_KEY
    BLINKTRADE_SECRET = settings_local.BLINKTRADE_SECRET
except ImportError:
    pass
