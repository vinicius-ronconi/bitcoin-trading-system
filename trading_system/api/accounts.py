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
        print response
        balance = beans.Balance(currency=None, currency_locked=None, btc=None, btc_locked=None)
        for broker_item in response['Responses']:
            if broker_item[str(self.client.broker)]:
                broker = broker_item[str(self.client.broker)]
                balance = beans.Balance(
                    currency=self.client.get_currency_value(broker.get(self.client.currency)),
                    currency_locked=self.client.get_currency_value(
                        broker.get('{currency}_locked'.format(currency=self.client.currency))
                    ),
                    btc=self.client.get_currency_value(broker.get('BTC')),
                    btc_locked=self.client.get_currency_value(broker.get('BTC_locked')),
                )

        return balance
