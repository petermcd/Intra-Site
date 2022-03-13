from urllib.parse import urlparse

from automation.dns import DNS
from automation.monitoring import Monitoring
from settings.models import Setting


class Automation:
    instance = None

    __slots__ = (
        "_dns",
        "_monitoring",
    )

    def __init__(self):
        """
        Standard init.
        """
        self._dns = None
        self._monitoring = None

    def __new__(cls):
        """
        Creates a singleton Automation.
        """
        if not hasattr(cls, "instance") or not cls.instance:
            cls.instance = super(Automation, cls).__new__(cls)
        return cls.instance

    def update_dns(self, hostname: str, ip: str, dns_provider: str):
        """
        Update a DNS record.

        Args:
            hostname: The hostname to be created/updated
            ip: IP the DNS record should point too
            dns_provider: DNS provider record needs creating on
        """
        self.dns.add_record(hostname=hostname, ip=ip, dns_provider=dns_provider)

    def delete_dns(self, hostname: str, dns_provider: str):
        """
        Delete a DNS record.

        Args:
            hostname: The hostname to be deleted
            dns_provider: DNS provider record needs creating on
        """
        self.dns.delete_record(hostname=hostname, dns_provider=dns_provider)

    def create_device_monitoring(self, device_details):
        """
        Create monitoring for a device.

        Args:
            device_details: Device to be created
        """
        self.monitoring.create_device(device_details)

    def update_device_monitoring(self, device_details):
        """
        Update monitoring for a device.

        Args:
            device_details: Device to be updated
        """
        self.monitoring.update_device(device_details)

    def delete_device_monitoring(self, device_details):
        """
        Remove monitoring for a device.

        Args:
            device_details: Device to be deleted
        """
        self.monitoring.delete_device(device_details)

    @staticmethod
    def get_hostname(url: str) -> str:
        """
        Obtains the hostname from a URL.

        Args
            url: URL to be parsed

        Return:
            Hostname part of a given URL
        """
        url_parts = urlparse(url)
        return url_parts.hostname or ""

    @property
    def dns(self) -> DNS:
        """
        Property to fetch DNS

        Returns:
             Instantiated DNS object
        """
        if not self._dns:
            api_key = Setting.objects.filter(name__exact="CLOUDFLARE_API_KEY")[0].value
            self._dns = DNS(api_key)
        return self._dns

    @property
    def monitoring(self) -> Monitoring:
        """
        Property to fetch DNS

        Returns:
             Instantiated Monitoring object
        """
        if not self._monitoring:
            url = Setting.objects.filter(name__exact="ZABBIX_URL")[0].value
            username = Setting.objects.filter(name__exact="ZABBIX_USERNAME")[0].value
            password = Setting.objects.filter(name__exact="ZABBIX_PASSWORD")[0].value
            self._monitoring = Monitoring(
                base_url=url, username=username, password=password
            )
        return self._monitoring
