from django.core.exceptions import ValidationError
from django.db import models
#from automation.automation import Automation


class AnsibleGroup(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name


class ConnectionMethod(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self) -> str:
        return self.name


class IP(models.Model):
    ip = models.GenericIPAddressField(unique=True)

    def __str__(self) -> str:
        return self.ip


class DeviceCategory(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self) ->str:
        return self.name


class DeviceType(models.Model):
    manufacturer = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    category = models.ForeignKey(DeviceCategory, on_delete=models.RESTRICT)

    def __str__(self) -> str:
        return f"{self.manufacturer} - {self.model}"


class Device(models.Model):
    name = models.CharField(max_length=255)
    hostname = models.CharField(max_length=255)
    mac_address = models.CharField(max_length=17, blank=True, null=True)
    ip = models.OneToOneField(IP, on_delete=models.CASCADE)
    device_type = models.ForeignKey(DeviceType, on_delete=models.CASCADE)
    description = models.CharField(max_length=500)
    connected_to = models.ForeignKey('self', on_delete=models.RESTRICT, blank=True, null=True)
    connection_method = models.ForeignKey(ConnectionMethod, on_delete=models.RESTRICT, blank=True, null=True)
    ansible_group = models.ManyToManyField(AnsibleGroup, blank=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self. _original_ip = self.ip

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.ip != self._original_ip:
            print('ip changed')


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

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.url and 'IP-ADDRESS.com' not in self.url:
            pass
            #automation = Automation()
            #required_dns = {
            #    'name': automation.get_hostname(self.url),
            #    'ip': self.hosted_on.ip.__str__()
            #}
            #automation.update_dns([required_dns,])

    @property
    def corrected_url(self) -> str:
        url = self.url
        if self.url and 'IP-ADDRESS.com' in self.url:
            url = url.replace('IP-ADDRESS.com', self.hosted_on.ip.__str__())
        return url
