import sys
sys.dont_write_bytecode = True
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Intranet.settings')
import django
django.setup()

from monzo.authentication import Authentication

from settings.models import Setting
from finance.models import Monzo, MONZO_REDIRECT_URL
from finance.views import MonzoStorage


monzo_auth = Authentication(
    client_id=self.client_id,
    client_secret=self.client_secret,
    redirect_url=MONZO_REDIRECT_URL,
    access_token=self.access_token,
)