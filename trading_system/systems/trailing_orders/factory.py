from trading_system.systems.trailing_orders.bootstrap import ManualInputBootstrap, FakeBootstrap


class TrailingOrdersFactory(object):
    @staticmethod
    def make_input_bootstrap():
        return ManualInputBootstrap()

    @staticmethod
    def make_fake_bootstrap(initial_setup):
        return FakeBootstrap(initial_setup)
