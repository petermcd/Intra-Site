# Turn off bytecode generation
import sys

sys.dont_write_bytecode = True

# Django specific settings
import os # NOQA E402

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Intranet.settings')
import django # NOQA E402

django.setup()

from monzo.authentication import Authentication # NOQA E402
from monzo.endpoints.account import Account # NOQA E402

from finance.models import MONZO_REDIRECT_URL, Monzo # NOQA E402
from finance.views import MonzoStorage # NOQA E402


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

    def fetch_transactions(self):
        accounts = Account.fetch(self._monzo_auth, 'uk_retail')
        print(accounts)


a = MonzoAutomation()
a.fetch_transactions()