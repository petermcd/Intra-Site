"""Models for the network application."""
from django.db import models


class AdditionalAnsibleGroup(models.Model):
    """Model for Ansible group."""

    name: models.CharField = models.CharField(max_length=255, unique=True)
    alias: models.CharField = models.CharField(max_length=255, blank=True)
    parent: models.ForeignKey = models.ForeignKey(
        "self", on_delete=models.RESTRICT, null=True, blank=True
    )
    description: models.TextField = models.TextField()

    def __str__(self):
        """Return the name of the group."""
        return self.name


class Application(models.Model):
    """Model for the application."""

    name: models.CharField = models.CharField(max_length=255, unique=True)
    alias: models.CharField = models.CharField(max_length=255, blank=True)
    description: models.TextField = models.TextField()

    class Meta:
        """Meta class."""

        verbose_name = "Application"
        verbose_name_plural = "Applications"

    def __str__(self):
        """Return the application name."""
        return self.name


class ConnectionType(models.Model):
    """Model for the connection type."""

    name: models.CharField = models.CharField(max_length=255, unique=True)
    unique_port: models.BooleanField = models.BooleanField(default=False)

    class Meta:
        """Meta class."""

        verbose_name = "Connection type"
        verbose_name_plural = "Connection types"

    def __str__(self):
        """Return the connection type name."""
        return self.name


class Registrar(models.Model):
    """Model for the registrar."""

    name: models.CharField = models.CharField(max_length=255, unique=True)
    url: models.URLField = models.URLField()

    class Meta:
        """Meta class."""

        verbose_name = "Registrar"
        verbose_name_plural = "Registrars"

    def __str__(self):
        """Return the registrar name."""
        return self.name


class DomainName(models.Model):
    """Model for the domain name."""

    name: models.CharField = models.CharField(max_length=255, unique=True)
    registrar: models.ForeignKey = models.ForeignKey(
        Registrar, on_delete=models.RESTRICT
    )

    class Meta:
        """Meta class."""

        verbose_name = "Domain name"
        verbose_name_plural = "Domain names"

    def __str__(self):
        """Return the domain name."""
        return self.name


class Vendor(models.Model):
    """Model for the vendor."""

    name: models.CharField = models.CharField(max_length=255, unique=True)
    url: models.URLField = models.URLField()

    class Meta:
        """Meta class."""

        verbose_name = "Vendor"
        verbose_name_plural = "Vendors"

    def __str__(self):
        """Return the vendor name."""
        return self.name


class Model(models.Model):
    """Model for the model."""

    name: models.CharField = models.CharField(max_length=255, unique=True)
    vendor: models.ForeignKey = models.ForeignKey(Vendor, on_delete=models.RESTRICT)

    class Meta:
        """Meta class."""

        verbose_name = "Model"
        verbose_name_plural = "Models"

    def __str__(self):
        """Return the model name."""
        return self.name


class DeviceType(models.Model):
    """Model for the device type."""

    name: models.CharField = models.CharField(max_length=255, unique=True)
    image: models.CharField = models.CharField(max_length=20)

    class Meta:
        """Meta class."""

        verbose_name = "Device type"
        verbose_name_plural = "Device types"

    def __str__(self):
        """Return the device type name."""
        return self.name


class OperatingSystem(models.Model):
    """Model for the operating system."""

    name: models.CharField = models.CharField(max_length=255, unique=True)
    alias: models.CharField = models.CharField(max_length=255, blank=True)
    vendor: models.ForeignKey = models.ForeignKey(Vendor, on_delete=models.RESTRICT)
    parent: models.ForeignKey = models.ForeignKey(
        "self", on_delete=models.RESTRICT, null=True, blank=True
    )
    default_username: models.CharField = models.CharField(
        max_length=255, null=True, blank=True
    )
    default_password: models.CharField = models.CharField(
        max_length=255, null=True, blank=True
    )

    class Meta:
        """Meta class."""

        verbose_name = "Operating system"
        verbose_name_plural = "Operating systems"

    def __str__(self):
        """Return the operating system name."""
        return self.name


class Device(models.Model):
    """Model for the device."""

    hostname: models.CharField = models.CharField(max_length=255, unique=True)
    ip_address: models.GenericIPAddressField = models.GenericIPAddressField(
        null=True, blank=True, unique=True
    )
    mac_address: models.CharField = models.CharField(
        max_length=255, null=True, blank=True, unique=True
    )
    operating_system: models.ForeignKey = models.ForeignKey(
        OperatingSystem, on_delete=models.RESTRICT
    )
    additional_ansible_groups: models.ManyToManyField = models.ManyToManyField(
        AdditionalAnsibleGroup,
        blank=True,
    )
    hardware_vendor: models.ForeignKey = models.ForeignKey(
        Vendor, on_delete=models.RESTRICT
    )
    model: models.ForeignKey = models.ForeignKey(Model, on_delete=models.RESTRICT)
    device_type: models.ForeignKey = models.ForeignKey(
        DeviceType, on_delete=models.RESTRICT
    )
    applications: models.ManyToManyField = models.ManyToManyField(
        Application, blank=True
    )
    connected_too: models.ForeignKey = models.ForeignKey(
        "self", on_delete=models.RESTRICT, null=True, blank=True
    )
    connection_type: models.ForeignKey = models.ForeignKey(
        ConnectionType, on_delete=models.RESTRICT
    )
    port: models.IntegerField = models.IntegerField(null=True, blank=True)
    rack_shelf: models.IntegerField = models.IntegerField(null=True, blank=True)
    rack_shelf_position: models.IntegerField = models.IntegerField(
        null=True, blank=True
    )
    description: models.TextField = models.TextField(null=True, blank=True)
    ansible_managed: models.BooleanField = models.BooleanField(default=True)
    wol: models.BooleanField = models.BooleanField(default=False)

    def __str__(self):
        """Return the device name."""
        return self.hostname

    class Meta:
        """Device` model meta class."""

        unique_together = [
            (
                "rack_shelf",
                "rack_shelf_position",
            ),
            (
                "connected_too",
                "port",
            ),
        ]
        verbose_name = "Device"
        verbose_name_plural = "Devices"


class AnsibleDeviceConfiguration(models.Model):
    """Model for the Ansible device configuration."""

    for_device: models.ForeignKey = models.ForeignKey(Device, on_delete=models.CASCADE)
    name: models.CharField = models.CharField(max_length=255)
    value: models.CharField = models.CharField(max_length=255)

    class Meta:
        """Meta class."""

        unique_together = [
            (
                "for_device",
                "name",
            ),
        ]
        verbose_name = "Ansible device configuration"
        verbose_name_plural = "Ansible device configurations"

    def __str__(self):
        """Return the Ansible device configuration name."""
        return f"{self.for_device.hostname} - {self.name}"


class Subdomain(models.Model):
    """Model for the subdomain."""

    name: models.CharField = models.CharField(max_length=255)
    domain_name: models.ForeignKey = models.ForeignKey(
        DomainName, on_delete=models.RESTRICT
    )
    hosted_on: models.ForeignKey = models.ForeignKey(Device, on_delete=models.RESTRICT)

    def __str__(self):
        """Return the subdomain name."""
        return self.name

    class Meta:
        """Subdomain` model meta class."""

        unique_together = [
            (
                "name",
                "domain_name",
            ),
        ]
        verbose_name = "Subdomain"
        verbose_name_plural = "Subdomains"


class Website(models.Model):
    """Model for the website."""

    name: models.CharField = models.CharField(max_length=255, unique=True)
    subdomain: models.ForeignKey = models.ForeignKey(
        Subdomain, on_delete=models.RESTRICT
    )
    secure: models.BooleanField = models.BooleanField(default=True)
    port: models.IntegerField = models.IntegerField(null=True, blank=True)
    path: models.CharField = models.CharField(max_length=255, null=True, blank=True)
    description: models.TextField = models.TextField(null=True, blank=True)

    class Meta:
        """Meta class."""

        verbose_name = "Website"
        verbose_name_plural = "Websites"

    def __str__(self):
        """Return the website name."""
        return self.name

    @property
    def full_url(self):
        """Return the full url."""
        port = f":{self.port}" if self.port else ""
        path = self.path or ""
        protocol = "https" if self.secure else "http"
        return f"{protocol}://{self.subdomain.name}.{self.subdomain.domain_name.name}{port}{path}"
