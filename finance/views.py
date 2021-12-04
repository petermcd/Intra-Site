from django.views import generic
from finance.models import Monzo, MONZO_REDIRECT_URL

from typing import Dict, Union

from monzo.authentication import Authentication
from monzo.handlers.storage import Storage
from monzo.exceptions import MonzoAuthenticationError


class MonzoStorage(Storage):
    """
    Class to implement the Monzo API Storage handler
    """
    def store(self, access_token: str, expiry: int, refresh_token: str = '') -> None:
        """
        Store the API tokens in the Django model.

        Args:
            access_token: API access token
            expiry: API Token expiry
            refresh_token: API refresh token
        """
        monzo_record = Monzo.objects.all()[0]
        monzo_record.access_token = access_token
        monzo_record.expiry = expiry
        monzo_record.refresh_token = refresh_token
        monzo_record.save()


class MonzoAuthView(generic.TemplateView):
    """
    Class to handle the Monzo authentication callback view.
    """
    template_name = 'admin/monzo/monzo.html'

    def get_context_data(self) -> Dict[str, Union[bool, str]]:
        """
        Prepare the context view to output.

        Return:
            Authentication result
        """
        return self._validate_monzo()

    def _validate_monzo(self) -> Dict[str, Union[bool, str]]:
        """
        Validate and process the authentication request.

        Return:
            Authentication result
        """
        monzo_record = Monzo.objects.all()
        if not monzo_record:
            context = {'success': False, 'error': 'Monzo is not configured'}
            return context
        monzo_auth = Authentication(
            client_id=monzo_record[0].client_id,
            client_secret=monzo_record[0].client_secret,
            redirect_url=MONZO_REDIRECT_URL,
            access_token=monzo_record[0].access_token,
            )
        handler = MonzoStorage()
        monzo_auth.register_callback_handler(handler)
        authorization_token = self.request.GET['code']
        state_token = self.request.GET['state']
        try:
            monzo_auth.authenticate(authorization_token=authorization_token, state_token=state_token)
            context = {'success': True, 'message': 'Remember to check your phone for alerts'}
        except MonzoAuthenticationError as exc:
            context = {'success': False, 'error': exc}

        return context


