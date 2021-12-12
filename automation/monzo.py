import sys

sys.dont_write_bytecode = True
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Intranet.settings')
import django

django.setup()

from monzo.authentication import Authentication

from finance.models import MONZO_REDIRECT_URL, Monzo
from finance.views import MonzoStorage
from settings.models import Setting

monzo_auth = Authentication(
    client_id=self.client_id,
    client_secret=self.client_secret,
    redirect_url=MONZO_REDIRECT_URL,
    access_token=self.access_token,
)