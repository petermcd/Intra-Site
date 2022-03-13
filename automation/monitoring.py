"""Monitoring logic."""
from pyzabbix import ZabbixAPI


class Monitoring:
    """Class to handle monitoring automation."""

    def __init__(self, base_url: str, username: str, password: str):
        """
        Initialize for Monitoring.

        Args:
            base_url: Zabbix APi URL
            username: Zabbix API username
            password: Zabbix API password
        """
        self._zabbix = ZabbixAPI(base_url)
        self._zabbix.session.verify = False
        self._zabbix.login(username, password)

    def delete_device(self, device_details):
        """
        Delete device monitoring.

        Args:
            device_details: Device to delete
        """
        device = self._fetch_device(device_details)
        if not device:
            return
        self._zabbix.host.delete(device["hostid"])

    def create_device(self, device_details):
        """
        Create monitoring for a new device.

        Args:
            device_details: Device to monitor
        """
        groups = self._format_groups(device_details)
        templates, _ = self._format_templates(device_details)
        self._zabbix.host.create(
            host=device_details["hostname"],
            name=device_details["name"],
            templates=templates,
            groups=groups,
            inventory_mode=1,
            interfaces=device_details["interfaces"],
        )

    def update_device(self, device_details):
        """
        Update a given device.

        Args:
            device_details: Device and details to update
        """
        device = self._fetch_device(device_details)
        interfaces = self._fetch_device_interfaces(device)
        interface_ids = [inter["type"] for inter in interfaces]
        missing_interfaces = [
            inter
            for inter in device_details["interfaces"]
            if str(inter["type"]) not in interface_ids
        ]
        self._add_device_interface(device, missing_interfaces)
        if not device:
            self.create_device(device_details)
            return
        required_templates, templates_to_clear = self._format_templates(
            device_details, device
        )
        groups = self._format_groups(device_details)
        self._zabbix.host.update(
            hostid=device["hostid"],
            hostname=device_details["hostname"],
            name=device_details["name"],
            templates=required_templates,
            groups=groups,
            templates_clear=templates_to_clear,
        )

    def _add_device_interface(self, device, interfaces):
        """
        Add a new interface to a device.

        Args:
            device: Device to add interface too
            interfaces: Interfaces to add
        """
        for interface in interfaces:
            self._zabbix.hostinterface.create(
                hostid=device["hostid"],
                **interface,
            )

    def _fetch_device(self, device):
        """
        Fetch device from the Zabbix monitoring platform.

        Args:
            device: Device to fetch
        """
        found_device = self._zabbix.host.get(
            filter={"host": device["hostname"]},
            selectParentTemplates=["templateid", "name"],
            selectGroups=["groupid", "name"],
        )
        if len(found_device) == 0:
            return None
        return found_device[0]

    def _fetch_device_interfaces(self, device):
        """
        Fetch device interfaces from the Zabbix monitoring platform.

        Args:
            device: Device to fetch
        """
        found_interface = self._zabbix.hostinterface.get(
            hostids=device["hostid"],
        )
        if len(found_interface) == 0:
            return None
        return found_interface

    @staticmethod
    def _format_templates(new_device_details, device=None):
        """
        Format a list of templates ready for the Zabbix API.

        Args:
            new_device_details: Device details
            device: Existing device
        """
        if not device:
            device = {}
        required_template_ids = []
        required_templates = []
        for template in new_device_details["templates"]:
            required_template_ids.append(template)
            required_templates.append({"templateid": template})
        templates_to_clear = [
            {"templateid": int(template["templateid"])}
            for template in device.get("parentTemplates", {})
            if int(template["templateid"]) not in required_template_ids
        ]

        return required_templates, templates_to_clear

    @staticmethod
    def _format_groups(new_device_details):
        """
        Format a list of groups ready for the Zabbix API.

        Args:
            new_device_details: Device details
        """
        groups = [{"groupid": group} for group in new_device_details["groups"]]
        if not groups:
            groups.append({"groupid": 19})
        return groups
