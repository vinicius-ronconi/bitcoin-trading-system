BLINKTRADE_KEY = 'my_api_key'
BLINKTRADE_SECRET = 'my_api_secret'

try:
    from .settings_local import *
except ImportError:
    pass
