from trading_system.api import beans
from trading_system.api import consts
from trading_system.api import exceptions
from trading_system.api.interfaces import IOrdersApi


class BlinkTradeOrdersApi(IOrdersApi):
    def __init__(self, client):
        """
        :type client: trading_system.api.clients.BlinkTradeClient
        """
        self.client = client

    def buy_bitcoins(self, order_type, price, quantity):
        return self._place_order(consts.OrderSide.BUY, order_type, price, quantity)

    def sell_bitcoins(self, order_type, price, quantity):
        return self._place_order(consts.OrderSide.SELL, order_type, price, quantity)

    def _place_order(self, order_side, order_type, price, quantity):
        msg = {
            'MsgType': consts.MessageType.PLACE_ORDER,
            'ClOrdID': self.client.get_unique_id(),
            'Symbol': consts.CURRENCY_TO_PAIR_MAP[self.client.currency],
            'Side': order_side,
            'OrdType': order_type,
            'Price': self.client.get_satoshi_value(price),
            'OrderQty': self.client.get_satoshi_value(quantity),
            'BrokerID': self.client.broker,
        }
        response = self.client.send_request(msg)
        self._validate_response(response)
        return self._parse_order_response(response)

    def cancel_order(self, order_id):
        msg = {
            'MsgType': consts.MessageType.CANCEL_ORDER,
            'ClOrdID': order_id,
        }
        response = self.client.send_request(msg)
        self._validate_response(response)
        return self._parse_order_response(response)

    @staticmethod
    def _validate_response(response):
        response_item = response['Responses'][0]
        if response_item.get('OrdStatus') == consts.OrderStatus.REJECTED:
            raise exceptions.OrderRejectedException('Unable to place the order', response_item)

    def _parse_order_response(self, response):
        order_response = [r for r in response['Responses'] if r['MsgType'] == consts.MessageType.PLACE_ORDER_RESPONSE]
        order_response = order_response[0] if order_response else None
        order_response = beans.PlacedOrder(
            order_id=long(order_response.get('OrderID')),
            time_in_force=str(order_response.get('TimeInForce')),
            exec_id=long(order_response.get('ExecID')),
            exec_type=str(order_response.get('ExecType')),
            order_status=str(order_response.get('OrdStatus')),
            cum_quantity=long(order_response.get('CumQty')),
            price=long(order_response.get('Price')),
            symbol=str(order_response.get('Symbol')),
            order_quantity=long(order_response.get('OrderQty')),
            last_shares=long(order_response.get('LastShares')),
            last_px=long(order_response.get('LastPx')),
            cxl_quantity=long(order_response.get('CxlQty')),
            volume=long(order_response.get('Volume')) if order_response.get('Volume') else None,
            leaves_quantity=long(order_response.get('LeavesQty')),
            message_type=str(order_response.get('MsgType')),
            exec_side=str(order_response.get('ExecSide')),
            order_type=str(order_response.get('OrdType')),
            order_rejection_reason=str(order_response.get('OrdRejReason')),
            side=str(order_response.get('Side')),
            client_order_id=long(order_response.get('ClOrdID')),
            average_px=long(order_response.get('AvgPx')),
        )

        balance_response = [r for r in response['Responses'] if r['MsgType'] == consts.MessageType.BALANCE_RESPONSE]
        balance_response = balance_response[0] if balance_response else None
        broker = balance_response[str(self.client.broker)]
        balance_response = beans.Balance(
            currency=self.client.get_currency_value(broker.get(self.client.currency)),
            currency_locked=self.client.get_currency_value(
                broker.get('{currency}_locked'.format(currency=self.client.currency))
            ),
            btc=self.client.get_currency_value(broker.get('BTC')),
            btc_locked=self.client.get_currency_value(broker.get('BTC_locked')),
        )

        return[order_response, balance_response]
