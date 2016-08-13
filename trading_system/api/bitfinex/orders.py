from trading_system import consts
from trading_system.api.beans import PlacedOrder
from trading_system.api.interfaces import IOrdersApi


class BitfinexOrdersApi(IOrdersApi):
    ORDER_TYPE = 'exchange limit'
    def __init__(self, client):
        """
        :type client: trading_system.api.bitfinex.clients.BitfinexClient
        """
        self.client = client

    def buy_bitcoins_with_limited_order(self, price, quantity):
        side = consts.ORDER_SIDE_TO_TEXT_MAP[consts.OrderSide.BUY]
        response = self.client.trade_api.place_order(str(quantity), str(price), side, self.ORDER_TYPE)
        return self._make_placed_order_from_response(response)

    def sell_bitcoins_with_limited_order(self, price, quantity):
        side = consts.ORDER_SIDE_TO_TEXT_MAP[consts.OrderSide.SELL]
        response = self.client.trade_api.place_order(str(quantity), str(price), side, self.ORDER_TYPE)
        print(response)
        return self._make_placed_order_from_response(response)

    def cancel_order(self, order_id):
        response = self.client.trade_api.delete_order(order_id)
        return self._make_placed_order_from_response(response)

    def get_pending_orders(self, page, page_size):
        orders = self.client.trade_api.active_orders()
        orders = [self._make_placed_order_from_response(order) for order in orders]
        return orders[page * page_size: (page + 1) * page_size - 1]

    def _make_placed_order_from_response(self, response):
        # TODO Check what is real global and what varies according to the exchange.
        # TODO Probably create consts specific to each exchange and create a map to the global option
        # TODO Examples: exec_type, order_status, order_side
        # TODO Replace volume with amount
        return PlacedOrder(
            order_id=self._get_str_value_or_none(response, 'order_id'),
            exec_id=str(response['id']),
            exec_type=response['type'],
            order_status=self._get_order_status(response),
            price=float(response['price']),
            symbol=str(response['symbol']).upper(),
            amount=float(response['original_amount']),
            message_type=None,
            order_rejection_reason=None,
            side=response['side'],
            client_order_id=self._get_str_value_or_none(response, 'order_id'),
        )

    @staticmethod
    def _get_str_value_or_none(source, key):
        value = source.get(key)
        return str(value) if value else None

    @staticmethod
    def _get_order_status(order):
        if order['is_cancelled']:
            return consts.OrderStatus.CANCELLED

        if order['is_live']:
            return consts.OrderStatus.NEW

