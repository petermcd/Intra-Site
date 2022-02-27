import re

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from automation.automation import Automation


class Playbook(models.Model):
    """
    Model for playbook.
    """
    name: models.CharField = models.CharField('Playbook', max_length=50, unique=True, blank=False, null=False)
    description: models.CharField = models.CharField(
        'description',
        max_length=2000,
        unique=False,
        blank=False,
        null=False
    )
    playbook: models.TextField = models.TextField('playbook', max_length=10000, unique=False, blank=False, null=False)

    def __str__(self) -> str:
        """
        To string method.

        Returns:
            string representation of the object.
        """
        return str(self.name)

    class Meta:
        ordering = ('name',)


class Application(models.Model):
    """
    Model for applications.
    """
    name: models.CharField = models.CharField('Application', max_length=200, unique=True, blank=False, null=False)
    description: models.CharField = models.CharField(
        'description',
        max_length=2000,
        unique=False,
        blank=False,
        null=False
    )
    parent: models.ForeignKey = models.ForeignKey('Application', on_delete=models.RESTRICT, null=True, blank=True)
    with_playbook: models.ForeignKey = models.ForeignKey(Playbook, on_delete=models.RESTRICT, null=True, blank=True)

    def __str__(self) -> str:
        """
        To string method.

        Returns:
            string representation of the object.
        """
        return str(self.name)

    @property
    def name_clean(self) -> str:
        """
        Property for the application name cleaned.

        Returns:
            Clean version of the application name
        """
        return re.sub('[^A-Za-z0-9_]', '_', str(self.name))

    class Meta:
        ordering = ('name',)


class DeviceType(models.Model):
    """
    Model for device type.
    """
    name: models.CharField = models.CharField('Device Type', max_length=200, unique=True, blank=False, null=False)
    image: models.CharField = models.CharField('Image', max_length=50, unique=False, blank=False, null=False)

    def __str__(self) -> str:
        """
        To string method.

        Returns:
            string representation of the object.
        """
        return str(self.name)

    class Meta:
        ordering = ('name',)


class Manufacturer(models.Model):
    """
    Model for device manufacturer.
    """
    name: models.CharField = models.CharField('Manufacturer', max_length=200, unique=True, null=False)
    url: models.URLField = models.URLField('URL', max_length=200, unique=True, null=False)

    def __str__(self) -> str:
        """
        To string method.

        Returns:
            string representation of the object.
        """
        return str(self.name)

    class Meta:
        ordering = ('name',)


class Model(models.Model):
    """
    Model for device model.
    """
    name: models.CharField = models.CharField('Model', max_length=200, unique=True, null=False)
    manufacturer: models.ForeignKey = models.ForeignKey(
        Manufacturer,
        on_delete=models.RESTRICT,
        null=False,
        blank=False
    )

    def __str__(self) -> str:
        """
        To string method.

        Returns:
            string representation of the object.
        """
        return f'{self.manufacturer.name} - {self.name}'

    class Meta:
        ordering = ('name',)


class Vendor(models.Model):
    """
    Model for operating system vendor.
    """
    name: models.CharField = models.CharField('Vendor', max_length=200, unique=True, null=False)
    url: models.URLField = models.URLField('URL', max_length=200, unique=True, null=False)

    def __str__(self) -> str:
        """
        To string method.

        Returns:
            string representation of the object.
        """
        return str(self.name)

    class Meta:
        ordering = ('name',)


class OperatingSystem(models.Model):
    """
    Model for operating system.
    """
    name: models.CharField = models.CharField('Name', max_length=100, null=False, blank=False)
    version: models.CharField = models.CharField('Version', max_length=10, null=False, blank=False)
    vendor: models.ForeignKey = models.ForeignKey(Vendor, on_delete=models.RESTRICT, null=False, blank=False)
    parent: models.ForeignKey = models.ForeignKey('OperatingSystem', on_delete=models.RESTRICT, null=True, blank=True)
    with_playbook: models.ForeignKey = models.ForeignKey(Playbook, on_delete=models.RESTRICT, null=True, blank=True)
    username: models.CharField = models.CharField('Username', max_length=100, null=True, blank=True)
    password: models.CharField = models.CharField('Password', max_length=100, null=True, blank=True)

    def __str__(self) -> str:
        """
        To string method.

        Returns:
            string representation of the object.
        """
        return f'{self.vendor.name} - {self.name} - {self.version}'

    @property
    def name_clean(self) -> str:
        """
        Property for the operating system name cleaned.

        Returns:
            Clean version of the operating system name
        """
        return re.sub('[^A-Za-z0-9_]', '_', str(self.name))

    class Meta:
        ordering = ('name',)


class ConnectionType(models.Model):
    """
    Model for connection types.
    """
    name: models.CharField = models.CharField('Connection Type', max_length=30, unique=True, null=False, blank=False)
    unique_port: models.BooleanField = models.BooleanField('Unique Port', default=True, null=False, blank=False)

    def __str__(self) -> str:
        """
        To string method.

        Returns:
            string representation of the object.
        """
        return str(self.name)

    class Meta:
        ordering = ('name',)


class Device(models.Model):
    """
    Model for device.
    """
    hostname: models.CharField = models.CharField('Hostname', max_length=200, unique=True, null=False)
    device_type: models.ForeignKey = models.ForeignKey(DeviceType, on_delete=models.RESTRICT, null=True, blank=True)
    ip: models.GenericIPAddressField = models.GenericIPAddressField('IP Address', unique=True, null=False, blank=False)
    mac_address: models.CharField = models.CharField('MAC Address', max_length=48, unique=True, null=True, blank=True)
    model: models.ForeignKey = models.ForeignKey(Model, on_delete=models.RESTRICT, null=False, blank=False)
    operating_system: models.ForeignKey = models.ForeignKey(
        OperatingSystem,
        on_delete=models.RESTRICT,
        null=False, blank=False
    )
    connected_via: models.ForeignKey = models.ForeignKey(
        ConnectionType,
        on_delete=models.RESTRICT,
        null=False,
        blank=False
    )
    connected_too: models.ForeignKey = models.ForeignKey(
        'Device',
        limit_choices_to={'switch_capable': True},
        on_delete=models.RESTRICT,
        null=True,
        blank=True
    )
    port: models.IntegerField = models.IntegerField('Port', default=0, null=False, blank=False)
    rack_shelf: models.IntegerField = models.IntegerField('Rack Shelf', null=True, blank=True)
    rack_shelf_position: models.IntegerField = models.IntegerField('Rack Shelf Position', null=True, blank=True)
    switch_capable: models.BooleanField = models.BooleanField('Switch Capable', default=False, null=False, blank=False)
    notes: models.CharField = models.CharField('Notes', max_length=1000, null=False, blank=False)
    installed_applications: models.ManyToManyField = models.ManyToManyField(Application, blank=True)
    __original_ip = None

    def __init__(self, *args, **kwargs):
        """
        Overridden init.
        """
        super(Device, self).__init__(*args, **kwargs)
        self.__original_ip = self.ip

    def clean(self):
        if self.connected_via.unique_port:
            matching_devices = Device.objects.all().filter(
                port__exact=self.port,
                connected_too=self.connected_too
            )
            pks = {matching_device.pk for matching_device in matching_devices}
            if self.port == 0:
                raise ValidationError({
                    'port': f'Post cannot be 0 for {self.connected_via.name}'
                })
            elif len(pks) > 0 and self.pk not in pks:
                device = Device.objects.get(id__exact=pks.pop())
                raise ValidationError({
                    'port': f'Port already in use by {device.hostname}.'
                })

    def __str__(self) -> str:
        """
        To string method.

        Returns:
            string representation of the object.
        """
        return str(self.hostname)

    def ip_changed(self) -> bool:
        """
        Check if IP has changed.

        returns:
        True if changed otherwise false
        """
        return self.__original_ip != self.ip

    class Meta:
        ordering = ('hostname',)


class Registrar(models.Model):
    """
    Model for registrar.
    """
    name: models.CharField = models.CharField('Registrar', max_length=30, unique=True, null=False, blank=False)
    url: models.URLField = models.URLField('URL', max_length=200, unique=True, null=False)

    def __str__(self) -> str:
        """
        To string method.

        Returns:
            string representation of the object.
        """
        return str(self.name)

    class Meta:
        ordering = ('name',)


class Domain(models.Model):
    """
    Model for domain.
    """
    name: models.CharField = models.CharField('Domain', max_length=30, unique=True, null=False, blank=False)
    registrar: models.ForeignKey = models.ForeignKey(Registrar, on_delete=models.RESTRICT, null=False, blank=False)

    def __str__(self) -> str:
        """
        To string method.

        Returns:
            string representation of the object.
        """
        return str(self.name)

    class Meta:
        ordering = ('name',)


class Subdomain(models.Model):
    """
    Model for subdomain.
    """
    name: models.CharField = models.CharField('Subdomain', max_length=30, unique=True, null=False, blank=False)
    domain: models.ForeignKey = models.ForeignKey(Domain, on_delete=models.RESTRICT, null=False, blank=False)
    hosted_on: models.ForeignKey = models.ForeignKey(Device, on_delete=models.RESTRICT, null=False, blank=False)
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
        return f'{self.name}.{self.domain.name}'

    def hosted_on_changed(self) -> bool:
        """
        Check if hosted on changed.

        Returns:
            True if changed otherwise False
        """
        return self.__originally_hosted_on != self.hosted_on

    class Meta:
        ordering = ('name',)


class Website(models.Model):
    """
    Model for subdomain.
    """
    name: models.CharField = models.CharField('Website', max_length=30, unique=True, null=False, blank=False)
    description: models.CharField = models.CharField('Description', max_length=1000, null=False, blank=False)
    secure: models.BooleanField = models.BooleanField('HTTPs', default=True, null=False, blank=False)
    subdomain: models.ForeignKey = models.ForeignKey(Subdomain, on_delete=models.RESTRICT, null=False, blank=False)
    port: models.IntegerField = models.IntegerField('Port', default=443, null=False, blank=False)
    path: models.CharField = models.CharField('Path', max_length=1000, default='/', null=False, blank=False)

    def __str__(self) -> str:
        """
        To string method.

        Returns:
            string representation of the object.
        """
        return str(self.name)

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

    class Meta:
        ordering = ('name',)


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
