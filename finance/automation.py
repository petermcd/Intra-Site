"""Class to support Monzo automation."""
from datetime import datetime, timedelta
from typing import Union

from monzo.authentication import Authentication
from monzo.endpoints.account import Account
from monzo.endpoints.transaction import Transaction

from finance.utilities import DjangoHandler


class MonzoAutomation:
    """Class to handle Monzo automation."""

    __slots__ = (
        "_account_id",
        "_auth",
        "_handler",
    )

    def __init__(self):
        """Initialise MonzoAutomation."""
        self._handler: DjangoHandler = DjangoHandler()
        credentials: dict[str, Union[int, str]] = self._handler.fetch()
        self._auth = Authentication(
            client_id=credentials["client_id"],
            client_secret=credentials["client_secret"],
            redirect_url="",
            access_token=credentials["access_token"],
            access_token_expiry=credentials["expiry"],
            refresh_token=credentials["refresh_token"],
        )

    def process(self):
        """Process transactions."""
        self._fetch_account()
        self._fetch_transactions()

    def _fetch_account(self):
        """Identify the correct account."""
        accounts = Account.fetch(auth=self._auth)
        for account in accounts:
            if account.account_type() == "Current Account":
                self._account_id = account.account_id
                break

    def _fetch_transactions(self):
        """Fetch transactions from Monzo."""
        since = self._handler.last_transaction_datetime
        if not since:
            since = datetime.now() - timedelta(days=89)

        transactions = Transaction.fetch(
            auth=self._auth, account_id=self._account_id, since=since
        )
        print(transactions)
