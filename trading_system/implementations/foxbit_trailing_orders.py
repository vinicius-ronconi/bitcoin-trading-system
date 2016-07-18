import threading
from datetime import datetime
from trading_system import consts
from trading_system.api.clients import BlinkTradeClient
from trading_system.systems.settings import *
from trading_system.systems.trailing_orders import TrailingOrders


class FoxbitTrailingOrder(object):
    def __init__(self):
        client = BlinkTradeClient(
            consts.Environment.PRODUCTION,
            consts.Currency.BRAZILIAN_REAIS,
            consts.Broker.FOXBIT,
            BLINKTRADE_KEY, BLINKTRADE_SECRET
        )

        self.system = TrailingOrders(client)

    def run(self):
        try:
            self.system.run()
        except Exception, e:
            curr = datetime.now()
            print '{time} - {text} - {args}'.format(time=curr.strftime('%Y-%m-%d %H:%M:%S'), text=str(e), args=e.args)
        threading.Timer(3, self.run).start()


if __name__ == '__main__':
    FoxbitTrailingOrder().run()
