from typing import Dict, List
from urllib.parse import urlparse
from .dns import DNS
from network_topology.models import Settings


class Automation:
    def __init__(self):
        settings = Settings.objects.filter(name__exact='CLOUDFLARE_API_KEY')
        self._dns = DNS(settings[0].value)

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Automation, cls).__new__(cls)
        return cls.instance

    def update_dns(self, required_dns: List[Dict[str, str]]):
        for item in required_dns:
            if self._dns.has_record(item['name']):
                continue
            self._dns.add_record(item['name'], item['ip'])

    @staticmethod
    def get_hostname(url: str) -> str:
        """
        Obtaines the hostname from a URL

        :param url: URL to be parsed

        :return: Hostname part of a given URL
        """
        url_parts = urlparse(url)
        return url_parts.hostname
