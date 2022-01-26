from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from automation.automation import Automation


class Manufacturer(models.Model):
    """
    Model for device manufacturer.
    """
    name = models.CharField('Manufacturer', max_length=200, unique=True, null=False)
    url = models.URLField('URL', max_length=200, unique=True, null=False)

    def __str__(self) -> str:
        """
        To string method.

        Returns:
            string representation of the object.
        """
        return self.name


class Model(models.Model):
    """
    Model for device model.
    """
    name = models.CharField('Model', max_length=200, unique=True, null=False)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.RESTRICT, null=False, blank=False)

    def __str__(self) -> str:
        """
        To string method.

        Returns:
            string representation of the object.
        """
        return self.name


class Vendor(models.Model):
    """
    Model for operating system vendor.
    """
    name = models.CharField('Vendor', max_length=200, unique=True, null=False)
    url = models.URLField('URL', max_length=200, unique=True, null=False)

    def __str__(self) -> str:
        """
        To string method.

        Returns:
            string representation of the object.
        """
        return self.name


class OperatingSystem(models.Model):
    """
    Model for operating system.
    """
    name = models.CharField('Name', max_length=100, null=False, blank=False)
    version = models.CharField('Version', max_length=10, null=False, blank=False)
    vendor = models.ForeignKey(Vendor, on_delete=models.RESTRICT, null=False, blank=False)

    def __str__(self) -> str:
        """
        To string method.

        Returns:
            string representation of the object.
        """
        return f'{self.vendor.name} - {self.name} - {self.version}'


class ConnectionTypes(models.Model):
    """
    Model for connection types.
    """
    name = models.CharField('Connection Type', max_length=30, unique=True, null=False, blank=False)
    unique_port = models.BooleanField('Unique Port', default=True, null=False, blank=False)

    def __str__(self) -> str:
        """
        To string method.

        Returns:
            string representation of the object.
        """
        return self.name


class Device(models.Model):
    """
    Model for device.
    """
    hostname = models.CharField('Hostname', max_length=200, unique=True, null=False)
    mac_address = models.CharField('MAC Address', max_length=48, unique=True, null=True, blank=True)
    ip = models.GenericIPAddressField('IP Address', unique=True, null=False, blank=False)
    model = models.ForeignKey(Model, on_delete=models.RESTRICT, null=False, blank=False)
    operating_system = models.ForeignKey(OperatingSystem, on_delete=models.RESTRICT, null=False, blank=False)
    connected_via = models.ForeignKey(ConnectionTypes, on_delete=models.RESTRICT, null=False, blank=False)
    connected_too = models.ForeignKey('Device', on_delete=models.RESTRICT, null=True, blank=True)
    port = models.IntegerField('Port', default=0, null=False, blank=False)
    rack_shelf = models.IntegerField('Rack Shelf', null=True, blank=True)
    rack_shelf_position = models.IntegerField('Rack Shelf Position', null=True, blank=True)
    notes = models.CharField('Notes', max_length=1000, null=False, blank=False)
    __original_ip = None

    def __init__(self, *args, **kwargs):
        """
        Overridden init.
        """
        super(Device, self).__init__(*args, **kwargs)
        self.__original_ip = self.ip

    def clean(self):
        matching_devices = Device.objects.all().filter(
            port__exact=self.port,
            connected_too=self.connected_too
        )
        hostnames = {matching_device.hostname for matching_device in matching_devices}
        if self.connected_via.unique_port:
            if self.port == 0:
                raise ValidationError({
                    'port': f'Post cannot be 0 for {self.connected_via.name}'
                })
            elif len(hostnames) > 0 and self.hostname not in hostnames:
                raise ValidationError({
                    'port': f'Port already in use by {hostnames.pop()}'
                })

    def __str__(self) -> str:
        """
        To string method.

        Returns:
            string representation of the object.
        """
        return self.hostname

    def ip_changed(self) -> bool:
        """
        Check if IP has changed.

        returns:
        True if changed otherwise false
        """
        return self.__original_ip != self.ip


class Registrar(models.Model):
    """
    Model for registrar.
    """
    name = models.CharField('Registrar', max_length=30, unique=True, null=False, blank=False)
    url = models.URLField('URL', max_length=200, unique=True, null=False)

    def __str__(self) -> str:
        """
        To string method.

        Returns:
            string representation of the object.
        """
        return self.name


class Domain(models.Model):
    """
    Model for domain.
    """
    name = models.CharField('Domain', max_length=30, unique=True, null=False, blank=False)
    registrar = models.ForeignKey(Registrar, on_delete=models.RESTRICT, null=False, blank=False)

    def __str__(self) -> str:
        """
        To string method.

        Returns:
            string representation of the object.
        """
        return self.name


class Subdomain(models.Model):
    """
    Model for subdomain.
    """
    name = models.CharField('Subdomain', max_length=30, unique=True, null=False, blank=False)
    domain = models.ForeignKey(Domain, on_delete=models.RESTRICT, null=False, blank=False)
    hosted_on = models.ForeignKey(Device, on_delete=models.RESTRICT, null=False, blank=False)
    __originally_hosted_on = None

    def __init__(self, *args, **kwargs):
        """
        Overridden init.
        """
        super(Subdomain, self).__init__(*args, **kwargs)
        if hasattr(self, 'hosted_on'):
            self.__originally_hosted_on = self.hosted_on

    @property
    def full_domain(self) -> str:
        """
        Property for full domain

        Returns:
            Concatenation of the domain and subdomain
        """
        return f'{self.name}.{self.domain.name}'

    def __str__(self) -> str:
        """
        To string method.

        Returns:
            string representation of the object.
        """
        return self.name

    def hosted_on_changed(self) -> bool:
        """
        Check if hosted on changed.

        Returns:
            True if changed otherwise False
        """
        return self.__originally_hosted_on != self.hosted_on


class Website(models.Model):
    """
    Model for subdomain.
    """
    name = models.CharField('Website', max_length=30, unique=True, null=False, blank=False)
    description = models.CharField('Description', max_length=1000, null=False, blank=False)
    secure = models.BooleanField('HTTPs', default=True, null=False, blank=False)
    subdomain = models.ForeignKey(Subdomain, on_delete=models.RESTRICT, null=False, blank=False)
    port = models.IntegerField('Port', default=443, null=False, blank=False)
    path = models.CharField('Path', max_length=1000, default='/', null=False, blank=False)

    def __str__(self) -> str:
        """
        To string method.

        Returns:
            string representation of the object.
        """
        return self.name

    @property
    def full_url(self) -> str:
        """
        Property to create the full URL.

        Returns:
            Full URL
        """
        schema = 'http://' if not self.secure else 'https://'
        port = f':{self.port}'
        if (self.secure and self.port == 443) or (not self.secure and port == 80):
            port = ''
        return f'{schema}{self.subdomain.full_domain}{port}{self.path}'


@receiver(post_save, sender=Device)
def device_subdomain_dns(sender, instance, **kwargs):
    """
    Trigger to update DNS when a device changes IP.

    Args:
        sender: Parent object
        instance: Instance object being updated
        kwargs: Not used but required by the API
    """
    if instance.ip_changed():
        auto = Automation()
        subdomains = Subdomain.objects.filter(hosted_on=instance)
        for subdomain in subdomains:
            auto.update_dns(
                hostname=subdomain.__str__(),
                ip=subdomain.device.ip,
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
    if instance.hosted_on_changed():
        auto = Automation()
        auto.update_dns(
            hostname=instance.name, ip=instance.hosted_on.ip, dns_provider=instance.domain.registrar.name
        )
