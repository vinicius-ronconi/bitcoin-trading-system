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

    @staticmethod
    def _validate_response(response):
        response_item = response['Responses'][0]
        if response_item.get('OrdStatus') == consts.OrderStatus.REJECTED:
            raise exceptions.OrderRejectedException('Unable to place the order', response_item)

    def _parse_order_response(self, response):
        order_responses = [r for r in response['Responses'] if r['MsgType'] == consts.MessageType.PLACE_ORDER_RESPONSE]
        order_list = []
        for order in order_responses:
            order_list.append(
                beans.PlacedOrder(
                    order_id=long(order.get('OrderID')),
                    time_in_force=str(order.get('TimeInForce')),
                    exec_id=long(order.get('ExecID')),
                    exec_type=str(order.get('ExecType')),
                    order_status=str(order.get('OrdStatus')),
                    cum_quantity=long(order.get('CumQty')),
                    price=long(order.get('Price')),
                    symbol=str(order.get('Symbol')),
                    order_quantity=long(order.get('OrderQty')),
                    last_shares=long(order.get('LastShares')),
                    last_px=long(order.get('LastPx')),
                    cxl_quantity=long(order.get('CxlQty')),
                    volume=long(order.get('Volume')) if order.get('Volume') else None,
                    leaves_quantity=long(order.get('LeavesQty')),
                    message_type=str(order.get('MsgType')),
                    exec_side=str(order.get('ExecSide')),
                    order_type=str(order.get('OrdType')),
                    order_rejection_reason=str(order.get('OrdRejReason')),
                    side=str(order.get('Side')),
                    client_order_id=long(order.get('ClOrdID')),
                    average_px=long(order.get('AvgPx')),
                )
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

        return order_list + [balance_response]

    def cancel_order(self, order_id):
        msg = {
            'MsgType': consts.MessageType.CANCEL_ORDER,
            'ClOrdID': order_id,
        }
        response = self.client.send_request(msg)
        self._validate_response(response)
        return self._parse_order_response(response)

    def get_pending_orders(self, page, page_size):
        return self._get_orders(orders_filter=['has_leaves_qty eq 1'], page=page, page_size=page_size)

    def get_executed_orders(self, page, page_size):
        return self._get_orders(orders_filter=['has_cum_qty eq 1'], page=page, page_size=page_size)

    def _get_orders(self, orders_filter, page=0, page_size=100):
        msg = {
            'MsgType': consts.MessageType.GET_ORDERS,
            'OrdersReqID': self.client.get_unique_id(),
            'Page': page,
            'PageSize': page_size,
            'Filter': orders_filter,

        }
        response = self.client.send_request(msg)
        self._validate_response(response)
        return self._parse_order_response(response)
