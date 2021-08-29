from pyzabbix import ZabbixAPI


class Monitoring:
    def __init__(self, base_url: str, username: str, password: str):
        self._zabbix = ZabbixAPI(base_url)
        self._zabbix.session.verify = False
        self._zabbix.login(username, password)

    def delete_device(self, device_details):
        device = self._fetch_device(device_details)
        if not device:
            return
        self._zabbix.host.delete(device['hostid'])

    def create_device(self, device_details):
        groups = self._format_groups(device_details)
        templates, _ = self._format_templates(device_details)
        self._zabbix.host.create(
            host=device_details['hostname'],
            name=device_details['name'],
            templates=templates,
            groups=groups,
            inventory_mode=1,
            interfaces=device_details['interfaces'],
        )

    def update_device(self, device_details):
        device = self._fetch_device(device_details)
        interfaces = self._fetch_device_interfaces(device)
        interface_ids = [inter['type'] for inter in interfaces]
        missing_interfaces = [
            inter
            for inter in device_details['interfaces']
            if str(inter['type']) not in interface_ids
        ]
        self._add_device_interface(device, missing_interfaces)
        if not device:
            self.create_device(device_details)
            return
        required_templates, templates_to_clear = self._format_templates(device_details, device)
        groups = self._format_groups(device_details)
        self._zabbix.host.update(
            hostid=device['hostid'],
            hostname=device_details['hostname'],
            name=device_details['name'],
            templates=required_templates,
            groups=groups,
            templates_clear=templates_to_clear,
        )

    def _add_device_interface(self, device, interfaces):
        for interface in interfaces:
            self._zabbix.hostinterface.create(
                hostid=device['hostid'],
                **interface,
            )

    def _fetch_device(self, device):
        found_device = self._zabbix.host.get(
            filter={'host': device['hostname']},
            selectParentTemplates=['templateid', 'name'],
            selectGroups=['groupid', 'name']
        )
        if len(found_device) == 0:
            return None
        return found_device[0]

    def _fetch_device_interfaces(self, device):
        found_interface = self._zabbix.hostinterface.get(
            hostids=device['hostid'],
        )
        if len(found_interface) == 0:
            return None
        return found_interface

    @staticmethod
    def _format_templates(new_device_details, device=None):
        if not device:
            device = {}
        required_template_ids = []
        required_templates = []
        for template in new_device_details['templates']:
            required_template_ids.append(template)
            required_templates.append({'templateid': template})
        templates_to_clear = [
            {'templateid': int(template['templateid'])}
            for template in device.get('parentTemplates', {})
            if int(template['templateid']) not in required_template_ids
        ]

        return required_templates, templates_to_clear

    @staticmethod
    def _format_groups(new_device_details):
        groups = [{'groupid': group} for group in new_device_details['groups']]
        if not groups:
            groups.append({'groupid': 19})
        return groups
