import os

BASE_DIR = os.path.dirname(__file__)

BITFINEX_KEY = 'my_api_key'
BITFINEX_SECRET = 'my_api_secret'

BLINKTRADE_KEY = 'my_api_key'
BLINKTRADE_SECRET = 'my_api_secret'

LOG_DIR = '{base_dir}/{log_dir}'.format(base_dir=BASE_DIR, log_dir='log')

try:
    from trading_system import settings_local

    BITFINEX_KEY = settings_local.BITFINEX_KEY
    BITFINEX_SECRET = settings_local.BITFINEX_SECRET

    BLINKTRADE_KEY = settings_local.BLINKTRADE_KEY
    BLINKTRADE_SECRET = settings_local.BLINKTRADE_SECRET
except ImportError:
    settings_local = None
