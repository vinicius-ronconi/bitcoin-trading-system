from trading_system.api.factory import ApiClientFactory
from trading_system.systems.executor import SystemExecutor
from trading_system.systems.trailing_orders.system import TrailingOrders
from trading_system.systems.trailing_orders.factory import TrailingOrdersFactory


class TrailingOrderImpl(object):
    def __init__(self, client_type):
        client = ApiClientFactory().make_client(client_type)
        bootstrap = TrailingOrdersFactory().make_input_bootstrap()
        self.system = TrailingOrders(client, bootstrap)

    def run(self):
        executor = SystemExecutor(self.system, interval=3)
        executor.execute()

if __name__ == '__main__':
    TrailingOrderImpl(ApiClientFactory.BITFINEX).run()
