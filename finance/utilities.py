"""Collection of classes and functions tp help normal activities."""
from datetime import datetime, timedelta
from typing import Optional, Union

from monzo.handlers.storage import Storage

from finance.models import Monzo


class DjangoHandler(Storage):
    """Class that will store credentials in the django database."""

    __instance = None
    _credentials_record = None

    def __new__(cls, *args, **kwargs):
        """Create a singleton instance."""
        if not cls.__instance:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def fetch(self) -> dict[str, Union[int, str]]:
        """
        Fetch Monzo credentials previously stored.

        Returns:
            Dictionary containing access token, expiry and refresh token
        """
        self._fetch_monzo_credential_object()
        return (
            {
                "access_token": str(self._credentials_record.access_token),
                "client_id": str(self._credentials_record.client_id),
                "client_secret": str(self._credentials_record.client_secret),
                "expiry": self._credentials_record.expiry,
                "refresh_token": str(self._credentials_record.access_token),
            }
            if self._credentials_record
            else {}
        )

    def set_client_details(self, client_id: str, client_secret: str):
        """
        Store a given client id and secret and clear all other details.

        Args:
            client_id: Client ID
            client_secret: Client secret
        """
        self._fetch_monzo_credential_object()
        if not self._credentials_record:
            return {}
        self._credentials_record.access_token = None
        self._credentials_record.client_id = client_id
        self._credentials_record.client_secret = client_secret
        self._credentials_record.expiry = None
        self._credentials_record.refresh_token = None
        self._credentials_record.last_fetched_datetime = None
        self._credentials_record.save()

    def store(
        self,
        access_token: str,
        client_id: str,
        client_secret: str,
        expiry: int,
        refresh_token: str = "",
    ) -> None:
        """
        Store the Monzo credentials.

        Args:
            access_token: New access token
            client_id: Monzo client ID
            client_secret: Monzo client secret
            expiry: Access token expiry as a unix timestamp
            refresh_token: Refresh token that can be used to renew the access token
        """
        self._fetch_monzo_credential_object()
        if not self._credentials_record:
            self._credentials_record = Monzo()
        self._credentials_record.access_token = access_token
        self._credentials_record.client_id = client_id
        self._credentials_record.client_secret = client_secret
        self._credentials_record.expiry = expiry
        self._credentials_record.refresh_token = refresh_token
        self._credentials_record.save()

    @property
    def configured(self) -> bool:
        """
        Check if Monzo has been configured.

        Returns:
            True if configured otherwise False
        """
        self._fetch_monzo_credential_object()
        return bool(self._credentials_record and self._credentials_record.expiry)

    @property
    def client_id(self) -> str:
        """
        Property for the Client ID.

        Returns:
            Client ID
        """
        self._fetch_monzo_credential_object()
        return (
            str(self._credentials_record.client_id) or ""
            if self._credentials_record
            else ""
        )

    @property
    def client_secret(self) -> str:
        """
        Property for the Client Secret.

        Returns:
            Client Secret
        """
        self._fetch_monzo_credential_object()
        return (
            str(self._credentials_record.client_secret) or ""
            if self._credentials_record
            else ""
        )

    @property
    def last_transaction_datetime(self) -> Optional[datetime]:
        """
        Property for the last transaction date/time.

        Returns:
            Last transaction date/time
        """
        self._fetch_monzo_credential_object()
        return (
            self._credentials_record.last_fetched_datetime
            if self._credentials_record
            else None
        )

    @last_transaction_datetime.setter
    def last_transaction_datetime(self, when: datetime) -> None:
        """
        Setter for last fetched date/time.

        Args:
            when: Date and time of the last fetched monzo transaction
        """
        # Increment when so we don't get the previous record again.
        if not self._credentials_record:
            self._credentials_record = Monzo()
        when += timedelta(seconds=1)
        self._credentials_record.last_fetched_datetime = when
        self._credentials_record.save()

    def _fetch_monzo_credential_object(self):
        """Fetch the monzo credential object from the database."""
        if self._credentials_record:
            return
        credentials: list[Monzo] = Monzo.objects.all()
        if len(credentials):
            self._credentials_record = credentials[0]
            return
        self._credentials_record = Monzo()


def create_redirect_url(request):
    """
    Build the URL to use for a redirect URL.

    Args:
        request: Object containing the full request details

    Returns:
        Redirect URL as a string
    """
    return f'{request.scheme}://{request.META["HTTP_HOST"]}{request.path}'
