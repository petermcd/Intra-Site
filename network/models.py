from django.db import models
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from automation.automation import Automation


class DeviceManufacturer(models.Model):
    """
    Model for device manufacturer.
    """
    name = models.CharField('Manufacturer', max_length=200, unique=True, null=False)
    url = models.URLField('URL', max_length=200, unique=True, null=False)
    notes = models.CharField('Notes', max_length=1000, null=True, blank=True)

    def __str__(self) -> str:
        """
        To string method.

        Returns:
            string representation of the object.
        """
        return self.name


class DeviceModel(models.Model):
    """
    Model for device model
    """
    model = models.CharField('Model', max_length=200, unique=True, null=False)
    notes = models.CharField('Notes', max_length=1000, null=True, blank=True)
    manufacturer = models.ForeignKey(DeviceManufacturer, on_delete=models.RESTRICT, null=False, blank=False)

    def __str__(self) -> str:
        """
        To string method.

        Returns:
            string representation of the object.
        """
        return f'{self.manufacturer} - {self.model}'


class DeviceType(models.Model):
    """
    Model for device type.
    """
    name = models.CharField('Device Type', max_length=200, unique=True, null=False)

    def __str__(self) -> str:
        """
        To string method.

        Returns:
            string representation of the object.
        """
        return self.name


class IP(models.Model):
    """
    Model for subnet.
    """
    address = models.GenericIPAddressField('IP Address', unique=True, null=False, blank=False)

    def __str__(self) -> str:
        """
        To string method.

        Returns:
            string representation of the object.
        """
        return self.address


class OperatingSystemVendor(models.Model):
    """
    Model for operating system vendor
    """
    name = models.CharField('Operating System Vendor', max_length=200, unique=True, null=False)
    url = models.URLField('URL', max_length=200, unique=True, null=False)

    def __str__(self) -> str:
        """
        To string method.

        Returns:
            string representation of the object.
        """
        return self.name


class OperatingSystemVersion(models.Model):
    """
    Model for operating system version
    """
    version = models.CharField('Version', max_length=200, unique=True, null=False)
    vendor = models.ForeignKey(OperatingSystemVendor, on_delete=models.RESTRICT, null=False, blank=False)

    def __str__(self) -> str:
        """
        To string method.

        Returns:
            string representation of the object.
        """
        return f'{self.vendor} - {self.version}'


class Registrar(models.Model):
    """
    Model for domain registrar.
    """
    name = models.CharField('Registrar', max_length=200, unique=True, null=False)
    url = models.URLField('URL', max_length=200, unique=True, null=False)

    def __str__(self) -> str:
        """
        To string method.

        Returns:
            string representation of the object.
        """
        return self.name


class Domains(models.Model):
    """
    Model for domain names.
    """
    name = models.CharField('Domain Name', max_length=200, unique=True, null=False)
    registrar = models.ForeignKey(Registrar, on_delete=models.RESTRICT, null=False, blank=False)

    def __str__(self) -> str:
        """
        To string method.

        Returns:
            string representation of the object.
        """
        return self.name

    class Meta:
        verbose_name_plural = 'Domains'


class Device(models.Model):
    """
    Model for devices.
    """
    hostname = models.CharField('Hostname', max_length=255, unique=True, null=False)
    ip = models.ForeignKey(IP, on_delete=models.RESTRICT, null=False, blank=False)
    notes = models.CharField('Notes', max_length=1000, null=True, blank=True)
    device_type = models.ForeignKey(DeviceType, on_delete=models.RESTRICT, null=False, blank=False)
    model = models.ForeignKey(DeviceModel, on_delete=models.RESTRICT, null=False, blank=False)
    operating_system = models.ForeignKey(OperatingSystemVersion, on_delete=models.RESTRICT, null=True, blank=True)
    connected_too = models.ForeignKey('Device', on_delete=models.RESTRICT, null=True, blank=True)
    __original_ip_id = None

    def __init__(self, *args, **kwargs):
        """
        Overridden init.
        """
        super(Device, self).__init__(*args, **kwargs)
        self.__original_ip_id = self.ip_id

    def __str__(self) -> str:
        """
        To string method.

        Returns:
            string representation of the object.
        """
        return self.hostname


class Subdomain(models.Model):
    """
    Model for subdomain
    """
    subdomain = models.CharField('Subdomain', max_length=200, unique=True, null=False)
    domain = models.ForeignKey(Domains, on_delete=models.RESTRICT, null=False, blank=False)
    device = models.ForeignKey(Device, on_delete=models.RESTRICT, null=False, blank=False)
    __original_device_id = None

    def __init__(self, *args, **kwargs):
        """
        Overridden init.
        """
        super(Subdomain, self).__init__(*args, **kwargs)
        self.__original_device_id = self.device_id

    def __str__(self) -> str:
        """
        To string method.

        Returns:
            string representation of the object.
        """
        return f'{self.subdomain}.{self.domain}'


class Website(models.Model):
    """
    Model for Website.
    """
    name = models.CharField('Name', max_length=255, unique=True, null=False)
    description = models.CharField('Description', max_length=1000, null=False, blank=False)
    secure = models.BooleanField('Secure', default=True, null=False, blank=False)
    subdomain = models.ForeignKey(Subdomain, on_delete=models.RESTRICT, null=False, blank=False)
    path = models.CharField('Path', max_length=200, unique=True, null=False)
    notes = models.CharField('Notes', max_length=1000, null=True, blank=True)

    def __str__(self) -> str:
        """
        To string method.

        Returns:
            string representation of the object.
        """
        protocol = 'https' if self.secure else 'http'
        return f'{protocol}://{self.subdomain}{self.path}'

    @property
    def full_url(self) -> str:
        """
        Websites full url.

        Returns:
            Full URL of website
        """
        return self.__str__()


@receiver(post_save, sender=Device)
def device_subdomain_dns(sender, instance, **kwargs):
    """
    Trigger to update DNS when a device changes IP.

    Args:
        sender: Parent object
        instance: Instance object being updated
        kwargs: Not used but required by the API
    """
    if instance._Device__original_ip_id != instance.ip_id:
        auto = Automation()
        subdomains = Subdomain.objects.filter(device=instance)
        for subdomain in subdomains:
            auto.update_dns(
                hostname=subdomain.__str__(),
                ip=subdomain.device.ip.address,
                dns_provider=subdomain.domain.registrar.name
            )


@receiver(post_delete, sender=Subdomain)
def subdomain_delete_dns(sender, instance, **kwargs):
    """
    Trigger to delete DNS when a subdomain is removed.

    Args:
        sender: Parent object
        instance: Instance object being updated
        kwargs: Not used but required by the API
    """
    auto = Automation()
    auto.delete_dns(hostname=instance.__str__(), dns_provider=instance.domain.registrar.name)


@receiver(post_save, sender=Subdomain)
def subdomain_save_dns(sender, instance, **kwargs):
    if instance.device_id != instance._Subdomain__original_device_id:
        auto = Automation()
        auto.update_dns(
            hostname=instance.__str__(), ip=instance.device.ip.address, dns_provider=instance.domain.registrar.name
        )
