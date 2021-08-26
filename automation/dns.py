from typing import Any, Dict, Optional

import CloudFlare


class DNS:
    _cf = None
    _cf_zones = {}
    _cf_domain = {}

    def __init__(self, api_key: str) -> None:
        """
        Creates the required API objects

        :param api_key: Cloudflare API Key
        """
        self._cf = CloudFlare.CloudFlare(token=api_key)

    def get_zone(self, domain: str) -> Optional[str]:
        """
        Retrieves the zones for the given domain

        :param domain: Domain we need the zone for

        :return: ID for the domain zone or None
        """
        if domain not in self._cf_zones.keys():
            zones = self._cf.zones.get(params={'name': domain})
            if len(zones) == 0:
                return None
            self._cf_zones[domain] = zones[0]['id']
        return self._cf_zones.get(domain, None)

    def get_record(self, domain: str, force: bool = False) -> Dict[str, Dict[str, Any]]:
        """
        Retrieves the DNS records for a given domain name

        :param domain: Domain DNS is required for
        :param force: If True will fetch even if records already obtained

        :return: Dictionary of DNS records for the given domain
        """
        if force or domain not in self._cf_domain.keys():
            domain_details = {}
            zone = self.get_zone(domain)
            if not zone:
                return {}
            domain_details['zone_id'] = zone
            dns_records = self._cf.zones.dns_records.get(domain_details['zone_id'])
            for dns_record in dns_records:
                domain_details[dns_record['name']] = dns_record
            self._cf_domain[domain] = domain_details
        return self._cf_domain[domain]

    def has_record(self, domain: str, ip: Optional[str] = None) -> bool:
        """
        Check to see if a domain currently has a specified dns record

        :param domain: Domain to check
        :param ip: IP the record should match

        :return: True if exists and IP match if specified
        """
        domain_details = self.split_domain(domain)
        records = self.get_record(domain_details['domain'])
        return domain in records and (not ip or records[domain]['content'] == ip)

    def add_record(self, dns_name: str, ip: str) -> None:
        """
        Creates a DNS record if it does not already exist

        :param dns_name: DNS Record to create
        :param ip: IP for DNS record to create
        """
        domain_details = self.split_domain(dns_name)
        zone_id = self.get_zone(domain_details['domain'])
        if not zone_id:
            return
        if self.has_record(domain=dns_name, ip=ip):
            return
        payload = {
            'name': domain_details['subdomain'],
            'type': 'A',
            'content': ip,
        }
        self._cf.zones.dns_records.post(zone_id, data=payload)

    def delete_record(self, dns_name) -> None:
        """
        Deletes a given DNS record

        :param dns_name: DNS name to be deleted
        """
        domain_details = self.split_domain(dns_name)
        zone_id = self.get_zone(domain_details['domain'])
        if not zone_id:
            return
        if not self.has_record(dns_name):
            return
        record_id = self._cf_domain[domain_details['domain']][dns_name]['id']
        self._cf.zones.dns_records.delete(zone_id, record_id)

    @staticmethod
    def split_domain(domain) -> Dict[str, str]:
        """
        Splits a domain into subdomain and domain components.

        :param domain: Domain to be split

        :return: Dict of domain and subdomain
        """
        domain_split = domain.split('.')
        subdomain = domain_split[0]
        domain = '.'.join(domain_split[1:])
        return {
            'subdomain': subdomain,
            'domain': domain,
        }
