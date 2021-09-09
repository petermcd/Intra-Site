from urllib.parse import urlparse

from automation.dns import DNS
from automation.monitoring import Monitoring


class Automation:
    instance = None

    def __init__(self, cloudflare_api_key: str, zabbix_url: str, zabbix_username: str, zabbix_password: str):
        """
        Standard init.

        Args:
            cloudflare_api_key: Cloudflare API key
            zabbix_url: API URL for Zabbix monitoring
            zabbix_username: API username for Zabbix monitoring
            zabbix_password: API password for Zabbix monitoring
        """
        self._dns = DNS(cloudflare_api_key)
        self._monitoring = Monitoring(zabbix_url, zabbix_username, zabbix_password)

    def __new__(cls, cloudflare_api_key: str, zabbix_url: str, zabbix_username: str, zabbix_password: str):
        """
        Creates a singleton Automation.

        Args:
            cloudflare_api_key: Cloudflare API key
            zabbix_url: API URL for Zabbix monitoring
            zabbix_username: API username for Zabbix monitoring
            zabbix_password: API password for Zabbix monitoring
        """
        if not hasattr(cls, 'instance'):
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
        self._dns.add_record(hostname=hostname, ip=ip, dns_provider=dns_provider)

    def delete_dns(self, hostname: str, dns_provider: str):
        """
        Delete a DNS record.

        Args:
            hostname: The hostname to be deleted
            dns_provider: DNS provider record needs creating on
        """
        self._dns.delete_record(hostname=hostname, dns_provider=dns_provider)

    def create_device_monitoring(self, device_details):
        """
        Create monitoring for a device.

        Args:
            device_details: Device to be created
        """
        self._monitoring.create_device(device_details)

    def update_device_monitoring(self, device_details):
        """
        Update monitoring for a device.

        Args:
            device_details: Device to be updated
        """
        self._monitoring.update_device(device_details)

    def delete_device_monitoring(self, device_details):
        """
        Remove monitoring for a device.

        Args:
            device_details: Device to be deleted
        """
        self._monitoring.delete_device(device_details)

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
        return url_parts.hostname or ''
