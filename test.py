# Turn off bytecode generation
import datetime
import sys

from typing import List

sys.dont_write_bytecode = True

# Django specific settings
import os  # NOQA E402

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Intranet.settings')
import django  # NOQA E402

django.setup()

from monzo.authentication import Authentication  # NOQA E402
from monzo.endpoints.account import Account  # NOQA E402

from monzo.endpoints.transaction import Transaction  # NOQA E402


from finance.models import MONZO_REDIRECT_URL, Monzo  # NOQA E402
from finance.views import MonzoStorage  # NOQA E402


class MonzoAutomation:
    __slots__ = [
        '_monzo_auth'
    ]

    def __init__(self):
        """
        Standard init to initiate required objects.
        """
        monzo_config = Monzo.objects.all()[0]
        self._monzo_auth = Authentication(
            client_id=monzo_config.client_id,
            client_secret=monzo_config.client_secret,
            redirect_url=MONZO_REDIRECT_URL,
            access_token=monzo_config.access_token,
            access_token_expiry=monzo_config.expiry,
            refresh_token=monzo_config.refresh_token,
        )
        handler = MonzoStorage()
        self._monzo_auth.register_callback_handler(handler)

    def fetch_accounts(self) -> List[Account]:
        return Account.fetch(auth=self._monzo_auth, account_type='uk_retail')

    def fetch_transactions(self, account: Account) -> List[Transaction]:
        today = datetime.date.today()
        since_date = today - datetime.timedelta(days=7)
        since = datetime.datetime(
            year=since_date.year,
            month=since_date.month,
            day=since_date.day,
        )
        return Transaction.fetch(
            auth=self._monzo_auth,
            account_id=account.account_id,
            since=since,
        )


a = MonzoAutomation()
accounts = a.fetch_accounts()
transactions = a.fetch_transactions(account=accounts[0])
print(transactions)
