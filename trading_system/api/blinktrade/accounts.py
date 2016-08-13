from trading_system.api import beans
from trading_system.api.interfaces import IAccountApi


class BlinkTradeAccountApi(IAccountApi):
    def __init__(self, client):
        """
        :type client: trading_system.api.blinktrade.clients.BlinkTradeClient
        """
        self.client = client

    def get_balance(self):
        balance = self.client.auth_api.get_balance()
        return self._make_balance_from_broker_dict(balance)

    def _make_balance_from_broker_dict(self, balance):
        """
        :type balance: dict
        :return: trading_system.api.beans.Balance
        """
        return beans.Balance(
            currency=balance.get(self.client.currency, 0),
            currency_locked=balance.get('{currency}_locked'.format(currency=self.client.currency), 0),
            btc=balance.get('BTC', 0),
            btc_locked=balance.get('BTC_locked', 0),
        )
