from trading_system.api.interfaces import IAccountApi
from trading_system.api.beans import Balance
from trading_system import consts


class BitfinexAccountApi(IAccountApi):
    def __init__(self, client):
        """
        :type client: trading_system.api.bitfinex.clients.BitfinexClient
        """
        self.client = client

    def get_balance(self):
        balance = self.client.auth_api.balances()
        return self._make_balance(balance)

    def _make_balance(self, balance_list):
        fiat_balance = self._get_currency_balance(balance_list, consts.Currency.AMERICAN_DOLLAR.lower())
        btc_balance = self._get_currency_balance(balance_list, consts.Currency.BITCOIN.lower())
        return Balance(
            currency=self._get_available_amount(fiat_balance),
            currency_locked=self._get_locked_amount(fiat_balance),
            btc=self._get_available_amount(btc_balance),
            btc_locked=self._get_locked_amount(btc_balance),
        )

    @staticmethod
    def _get_currency_balance(balance_list, currency):
        balance = [
            balance for balance in balance_list if balance['type'] == 'exchange' and balance['currency'] == currency
        ]
        return balance[0] if balance else {}

    @staticmethod
    def _get_available_amount(balance):
        return float(balance.get('available', 0))

    @staticmethod
    def _get_locked_amount(balance):
        return float(balance.get('amount', 0)) - float(balance.get('available', 0))
