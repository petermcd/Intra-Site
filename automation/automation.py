from typing import Dict, List
from urllib.parse import urlparse

from .dns import DNS
from .monitoring import Monitoring


class Automation:
    def __init__(self, cloudflare_api_key: str, zabbix_url: str, zabbix_username: str, zabbix_password: str):
        self._dns = DNS(cloudflare_api_key)
        self._monitoring = Monitoring(zabbix_url, zabbix_username, zabbix_password)

    def __new__(cls, cloudflare_api_key: str, zabbix_url: str, zabbix_username: str, zabbix_password: str):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Automation, cls).__new__(cls)
        return cls.instance

    def update_dns(self, required_dns: List[Dict[str, str]]):
        for item in required_dns:
            if self._dns.has_record(item['name']):
                continue
            self._dns.add_record(item['name'], item['ip'])

    def create_device_monitoring(self, device_details):
        self._monitoring.create_device(device_details)

    def update_device_monitoring(self, device_details):
        self._monitoring.update_device(device_details)

    def delete_device_monitoring(self, device_details):
        self._monitoring.delete_device(device_details)

    @staticmethod
    def get_hostname(url: str) -> str:
        """
        Obtaines the hostname from a URL

        :param url: URL to be parsed

        :return: Hostname part of a given URL
        """
        url_parts = urlparse(url)
        return url_parts.hostname
