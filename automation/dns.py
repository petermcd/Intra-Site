"""DNS logic."""
from typing import Any, Dict, Optional

import CloudFlare


class DNS:
    """Class to handle DNS updates."""

    __slots__ = ["_cf", "_cf_zones", "_cf_domain"]

    def __init__(self, api_key: str) -> None:
        """
        Create the required API objects.

        Args:
             api_key: Cloudflare API Key
        """
        self._cf_zones: Dict[str, Any] = {}
        self._cf_domain: Dict[str, Any] = {}
        self._cf = CloudFlare.CloudFlare(token=api_key)

    def get_zone(self, domain: str) -> Optional[str]:
        """
        Retrieve the zones for the given domain.

        Args:
            domain: Domain we need the zone for

        Return:
            ID for the domain zone or None
        """
        if domain not in self._cf_zones.keys():
            zones = self._cf.zones.get(params={"name": domain})
            if len(zones) == 0:
                return ""
            self._cf_zones[domain] = zones[0]["id"]
        return self._cf_zones.get(domain, None)

    def get_record(self, domain: str, force: bool = False) -> Dict[str, Dict[str, Any]]:
        """
        Retrieve the DNS records for a given domain name.

        Args:
            domain: Domain DNS is required for
            force: If True will fetch even if records already obtained

        Return:
            Dictionary of DNS records for the given domain
        """
        if force or domain not in self._cf_domain.keys():
            domain_details = {}
            zone = self.get_zone(domain)
            if not zone:
                return {}
            domain_details["zone_id"] = zone
            dns_records = self._cf.zones.dns_records.get(domain_details["zone_id"])
            for dns_record in dns_records:
                domain_details[dns_record["name"]] = dns_record
            self._cf_domain[domain] = domain_details
        return self._cf_domain[domain]

    def has_record(self, domain: str, ip: Optional[str] = None) -> bool:
        """
        Check to see if a domain currently has a specified dns record.

        Args:
            domain: Domain to check
            ip: IP the record should match

        Return:
            True if exists and IP match if specified
        """
        domain_details = self.split_domain(domain)
        records = self.get_record(domain_details["domain"])
        return domain in records and (not ip or records[domain]["content"] == ip)

    def add_record(self, hostname: str, ip: str, dns_provider: str) -> None:
        """
        Create a DNS record if it does not already exist.

        Args:
            hostname: DNS Record to create
            ip: IP for DNS record to create
            dns_provider: DNS Provider
        """
        domain_details = self.split_domain(hostname)
        zone_id = self.get_zone(domain_details["domain"])
        record_type = "A"

        if not zone_id:
            return

        if self.has_record(hostname, ip):
            return
        elif self.has_record(hostname):
            self.delete_record(hostname=hostname, dns_provider=dns_provider)

        name = domain_details["subdomain"]

        if domain_details["subdomain"].lower() == "www":
            payload = {
                "name": domain_details["subdomain"],
                "type": "CNAME",
                "content": domain_details["domain"],
            }
            self._cf.zones.dns_records.post(zone_id, data=payload)
            name = domain_details["domain"]

        payload = {
            "name": name,
            "type": record_type,
            "content": ip,
        }
        self._cf.zones.dns_records.post(zone_id, data=payload)

    def delete_record(self, hostname: str, dns_provider: str) -> None:
        """
        Delete a given DNS record.

        Args
            hostname: DNS name to be deleted
            dns_provider: DNS Provider
        """
        domain_details = self.split_domain(hostname)
        zone_id = self.get_zone(domain_details["domain"])
        if not zone_id:
            return
        if not self.has_record(hostname):
            return
        record_id = self._cf_domain[domain_details["domain"]][hostname]["id"]
        self._cf.zones.dns_records.delete(zone_id, record_id)

    @staticmethod
    def split_domain(domain) -> Dict[str, str]:
        """
        Split a domain into subdomain and domain components.

        Args:
            domain: Domain to be split

        Return:
            Dict of domain and subdomain
        """
        domain_split = domain.split(".")
        subdomain = domain_split[0]
        domain = ".".join(domain_split[1:])
        return {
            "subdomain": subdomain,
            "domain": domain,
        }
