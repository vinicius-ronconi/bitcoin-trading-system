from functools import partial

from trading_system import consts
from trading_system.api import beans
from trading_system.api import exceptions
from trading_system.api.interfaces import IOrdersApi


class BlinkTradeOrdersApi(IOrdersApi):
    def __init__(self, client):
        """
        :type client: trading_system.api.blinktrade.clients.BlinkTradeClient
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
            'Symbol': consts.CURRENCY_TO_SYMBOL_MAP[self.client.currency],
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
        order_list = self._get_orders_from_response(response)
        balance = self._get_balance_from_response(response)
        return order_list + [balance]

    def _get_orders_from_response(self, response):
        placed_orders_list = self._get_placed_order_from_response(response)
        order_status_list = self._get_order_status_from_response(response)
        return placed_orders_list + order_status_list

    def _get_placed_order_from_response(self, response):
        order_list = [r for r in response['Responses'] if r['MsgType'] == consts.MessageType.PLACE_ORDER_RESPONSE]
        return [self._make_placed_order_from_dict(order) for order in order_list]

    def _make_placed_order_from_dict(self, order):
        # TODO: Store price and volume as float values
        # TODO: Review order quantity x volume on responses, exec_type x order_type, exec_side x side
        return beans.PlacedOrder(
            order_id=str(order.get('OrderID')),
            exec_id=self._get_str_value_or_none(order, 'ExecID'),
            exec_type=order.get('ExecType'),
            order_status=order.get('OrdStatus'),
            price=self.client.get_decimal_value(self._get_int_value_or_none(order, 'Price')),
            symbol=order.get('Symbol'),
            amount=self.client.get_decimal_value(self._get_int_value_or_none(order, 'OrderQty')),
            message_type=order.get('MsgType'),
            order_rejection_reason=order.get('OrdRejReason'),
            side=order.get('Side'),
            client_order_id=str(order.get('ClOrdID')),
        )

    @staticmethod
    def _get_int_value_or_none(source, key):
        value = source.get(key)
        return int(value) if value else None

    @staticmethod
    def _get_str_value_or_none(source, key):
        value = source.get(key)
        return str(value) if value else None

    def _get_order_status_from_response(self, response):
        responses = [r for r in response['Responses'] if r['MsgType'] == consts.MessageType.ORDER_STATUS_RESPONSE]
        multilevel_order_list = [self._make_placed_order_from_order_status_response(response) for response in responses]
        flat_list = [item for sublist in multilevel_order_list for item in sublist]
        return flat_list

    def _make_placed_order_from_order_status_response(self, response):
        keys = response['Columns']
        values_list = response['OrdListGrp']
        partial_zip_func = partial(zip, keys)
        zipped_orders_list = map(partial_zip_func, values_list)
        dict_list = map(dict, zipped_orders_list)
        return map(self._make_placed_order_from_dict, dict_list)

    def _get_balance_from_response(self, response):
        balance_list = [r for r in response['Responses'] if r['MsgType'] == consts.MessageType.BALANCE_RESPONSE]
        if not balance_list:
            return None
        balance = balance_list[0]
        broker = balance[str(self.client.broker)]
        return beans.Balance(
            currency=self.client.get_decimal_value(broker.get(self.client.currency)),
            currency_locked=self.client.get_decimal_value(
                broker.get('{currency}_locked'.format(currency=self.client.currency))
            ),
            btc=self.client.get_decimal_value(broker.get('BTC')),
            btc_locked=self.client.get_decimal_value(broker.get('BTC_locked')),
        )

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
