from django.db import models


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
    url = models.URLField('URL', max_length=200, unique=True, null=False)
    subdomain = models.ForeignKey(Subdomain, on_delete=models.RESTRICT, null=False, blank=False)
    __original_subdomain_id = None
    __original_url = None

    def __init__(self, *args, **kwargs):
        """
        Overridden init.
        """
        super(Website, self).__init__(*args, **kwargs)
        self.__original_subdomain_id = self.subdomain_id
        self.__original_url = self.url

    def __str__(self) -> str:
        """
        To string method.

        Returns:
            string representation of the object.
        """
        return self.url

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.pk:
            print('new')
        print('aaa')
        super(Website, self).save(
            force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields
        )
