from trading_system.api import beans
from trading_system.api.interfaces import IOrdersApi


class BlinkTradeOrdersApi(IOrdersApi):
    def __init__(self, client):
        """
        :type client: trading_system.api.blinktrade.clients.BlinkTradeClient
        """
        self.client = client

    def buy_bitcoins_with_limited_order(self, price, quantity):
        response = self.client.auth_api.buy_bitcoins_with_limited_order(price, quantity)
        return self._parse_order_response(response)

    def sell_bitcoins_with_limited_order(self, price, quantity):
        response = self.client.auth_api.sell_bitcoins_with_limited_order(price, quantity)
        return self._parse_order_response(response)

    def _parse_order_response(self, response):
        order_list = [self._make_placed_order_from_dict(response[0])]
        balance = None if len(response) == 0 else self._make_balance(response[1])
        return order_list + [balance] if balance else order_list

    def _make_placed_order_from_dict(self, order):
        return beans.PlacedOrder(
            order_id=str(order.get('OrderID')),
            exec_id=self._get_str_value_or_none(order, 'ExecID'),
            exec_type=order.get('ExecType'),
            order_status=order.get('OrdStatus'),
            price=order.get('Price'),
            symbol=order.get('Symbol'),
            amount=order.get('OrderQty'),
            message_type=order.get('MsgType'),
            order_rejection_reason=order.get('OrdRejReason'),
            side=order.get('Side'),
            client_order_id=str(order.get('ClOrdID')),
        )

    @staticmethod
    def _get_str_value_or_none(source, key):
        value = source.get(key)
        return str(value) if value else None

    def _make_balance(self, balance):
        return beans.Balance(
            currency=balance.get(self.client.currency, 0),
            currency_locked=balance.get('{currency}_locked'.format(currency=self.client.currency), 0),
            btc=balance.get('BTC', 0),
            btc_locked=balance.get('BTC_locked', 0),
        )

    def cancel_order(self, order_id):
        response = self.client.auth_api.cancel_order(order_id)
        return self._parse_order_response(response)

    def get_pending_orders(self, page, page_size):
        response = self.client.auth_api.get_pending_orders(page, page_size)
        return list(map(self._make_placed_order_from_dict, response))
