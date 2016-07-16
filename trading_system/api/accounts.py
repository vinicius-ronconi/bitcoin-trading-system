from trading_system.api import beans
from trading_system.api import consts
from trading_system.api.interfaces import IAccountApi


class BlinkTradeAccountApi(IAccountApi):
    def __init__(self, client):
        """
        :type client: trading_system.api.clients.BlinkTradeClient
        """
        self.client = client

    def get_balance(self):
        msg = {
            'MsgType': consts.MessageType.BALANCE,
            'BalanceReqID': self.client.get_unique_id(),
        }
        response = self.client.send_request(msg)
        broker = [broker for broker in response['Responses'] if broker.get(str(self.client.broker))]
        return self._make_balance_from_broker_dict(broker)

    def _make_balance_from_broker_dict(self, broker):
        if broker:
            broker = broker[0]
            balance = beans.Balance(
                currency=self.client.get_currency_value(broker.get(self.client.currency)),
                currency_locked=self.client.get_currency_value(
                    broker.get('{currency}_locked'.format(currency=self.client.currency))
                ),
                btc=self.client.get_currency_value(broker.get('BTC')),
                btc_locked=self.client.get_currency_value(broker.get('BTC_locked')),
            )
        else:
            balance = beans.Balance(currency=None, currency_locked=None, btc=None, btc_locked=None)
        return balance
