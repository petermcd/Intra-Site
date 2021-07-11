from django.db import models
from django.db.models.signals import m2m_changed, post_delete, post_save
from django.dispatch import Signal, receiver

from automation.automation import Automation


class MonitoringGroup(models.Model):
    name = models.CharField(max_length=50)
    group_id = models.IntegerField()

    def __str__(self) -> str:
        return self.name


class ConnectionMethod(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self) -> str:
        return str(self.name)


class MonitoringTemplate(models.Model):
    name = models.CharField(max_length=255)
    template_id = models.IntegerField()

    def __str__(self):
        return self.name


class IP(models.Model):
    ip = models.GenericIPAddressField(unique=True)

    def __str__(self) -> str:
        return str(self.ip)


class DeviceCategory(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.name


class DeviceType(models.Model):
    manufacturer = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    category = models.ForeignKey(DeviceCategory, on_delete=models.RESTRICT)
    monitoring_templates = models.ManyToManyField(MonitoringTemplate, blank=True)

    def __str__(self) -> str:
        return f"{self.manufacturer} - {self.model}"


class Device(models.Model):
    name = models.CharField(max_length=255)
    hostname = models.CharField(max_length=255)
    mac_address = models.CharField(max_length=17, blank=True, null=True)
    ip = models.OneToOneField(IP, on_delete=models.CASCADE)
    device_type = models.ForeignKey(DeviceType, on_delete=models.CASCADE)
    description = models.CharField(max_length=500)
    snmp_enabled = models.BooleanField(default=False)
    connected_to = models.ForeignKey('self', on_delete=models.RESTRICT, blank=True, null=True)
    connection_method = models.ForeignKey(ConnectionMethod, on_delete=models.RESTRICT, blank=True, null=True)
    monitoring_groups = models.ManyToManyField(MonitoringGroup, blank=False)
    monitoring_templates = models.ManyToManyField(MonitoringTemplate, blank=True)

    def __str__(self) -> str:
        return self.name


class Settings(models.Model):
    name = models.CharField(max_length=255)
    value = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Site(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=1000)
    hosted_on = models.ForeignKey(Device, on_delete=models.RESTRICT, blank=True, null=True)
    url = models.URLField(null=True, blank=True)

    def __str__(self) -> str:
        return self.name

    @property
    def corrected_url(self) -> str:
        url = self.url
        if self.url and 'IP-ADDRESS.com' in self.url:
            url = url.replace('IP-ADDRESS.com', str(self.hosted_on.ip))
        return url


monitoring_update = Signal()
dns_update = Signal()


@receiver(post_save, sender=Site)
def site_update_dns(sender, instance, **kwargs):
    """
    Trigger for Site to update the DNS if required

    :param sender: Parent object
    :param instance: Instance object being updated
    :param kwargs: Not used but required by the API
    """
    device = instance.hosted_on
    dns_update.send(sender=Device, instance=device)


@receiver(post_save, sender=Device)
def device_update_dns(sender, instance, **kwargs):
    """
    Trigger for Device so that the site DNS can update if IP changes

    :param sender: Parent object
    :param instance: Instance object being updated
    :param kwargs: Not used but required by the API
    """
    sites = Site.objects.filter(hosted_on=instance)
    if len(sites) == 0:
        return
    automation = instantiate_automation()
    hosts = []
    tasks = []
    for site in sites:
        hostname = automation.get_hostname(site.url)
        if hostname not in hosts:
            hosts.append(hostname)
            tasks.append({
                'name': automation.get_hostname(site.url),
                'ip': str(instance.ip)
            })
    automation.update_dns(tasks)


@receiver(post_save, sender=Site)
@receiver(post_delete, sender=Site)
def site_update_monitoring(sender, instance, **kwargs):
    """
    Triggers when a site has been updated and triggers an update on device to ensure monitoring is upto date

    :param sender: Parent object
    :param instance: Instance object being updated
    :param kwargs: Not used but required by the API
    """
    device = instance.hosted_on
    monitoring_update.send(sender=Device, instance=device)


@receiver(post_save, sender=Device)
@receiver(monitoring_update)
def device_update_monitoring(sender, instance, **kwargs):
    """
    Updates monitoring for a device when it is updated

    :param sender: Parent object
    :param instance: Instance object being updated
    :param kwargs: Not used but required by the API
    """
    automation = instantiate_automation()
    interfaces = [
        {
            "type": 1,
            "main": 1,
            "useip": 1,
            "ip": str(instance.ip),
            "dns": "",
            "port": "10050"
        }
    ]
    if instance.snmp_enabled:
        snmp_username = Settings.objects.filter(name__exact='SNMP_USERNAME')[0].value
        snmp_password = Settings.objects.filter(name__exact='SNMP_PASSWORD')[0].value
        interfaces.append(
            {
                "type": 2,
                "main": 1,
                "useip": 1,
                "ip": str(instance.ip),
                "dns": "",
                "port": "161",
                'details': {
                    'version': 3,
                    'bulk': 1,
                    'securityname': snmp_username,
                    'securitylevel': 1,
                    'authpassphrase': snmp_password,
                    'contextname': '',
                }
            }
        )

    monitoring_templates = {
        template.template_id
        for template in instance.monitoring_templates.all()
    }

    for template in instance.device_type.monitoring_templates.all():
        monitoring_templates.add(template.template_id)
    monitoring_groups = {
        group.group_id for group in instance.monitoring_groups.all()
    }

    device_details = {
        'name': instance.name,
        'hostname': instance.hostname,
        'ip': str(instance.ip),
        'device_id': instance.pk,
        'templates': monitoring_templates,
        'groups': monitoring_groups,
        'interfaces': interfaces,
    }
    automation.update_device_monitoring(device_details)


@receiver(m2m_changed, sender=Device.monitoring_groups.through)
@receiver(m2m_changed, sender=Device.monitoring_templates.through)
def device_update_monitoring(sender, instance, **kwargs):
    monitoring_update.send(sender=Device, instance=instance)


@receiver(post_delete, sender=Device)
def device_delete_monitoring(sender, instance, **kwargs):
    """
    Trigger for Device so that the site monitoring can be removed if a device is deleted

    :param sender: Parent object
    :param instance: Instance object being updated
    :param kwargs: Not used but required by the API
    """
    automation = instantiate_automation()
    device_details = {
        'name': instance.name,
        'hostname': instance.hostname,
        'ip': str(instance.ip),
        'device_id': instance.pk,
        'templates': set(),
        'groups': set(),
        'interfaces': [],
    }
    automation.delete_device_monitoring(device_details)


@receiver(post_save, sender=DeviceType)
def device_type_update_monitoring(sender, instance, **kwargs):
    """
    Triggers when a site has been updated and triggers an update on device to ensure monitoring is upto date

    :param sender: Parent object
    :param instance: Instance object being updated
    :param kwargs: Not used but required by the API
    """
    devices = Device.objects.filter(device_type=instance)
    for device in devices:
        monitoring_update.send(sender=Device, instance=device)


def instantiate_automation() -> Automation:
    """
    Helper to create the Automation object with the correct parameters

    :return: An instantiated Automation object
    """
    credentials = {
        'cloudflare_api_key': Settings.objects.filter(name__exact='CLOUDFLARE_API_KEY')[0].value,
        'zabbix_url': Settings.objects.filter(name__exact='ZABBIX_URL')[0].value,
        'zabbix_username': Settings.objects.filter(name__exact='ZABBIX_USERNAME')[0].value,
        'zabbix_password': Settings.objects.filter(name__exact='ZABBIX_PASSWORD')[0].value,
    }
    return Automation(**credentials)
