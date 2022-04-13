"""Models for the network application."""
from django.db import models


class Application(models.Model):
    """Model for the application."""

    name: models.CharField = models.CharField(max_length=255, unique=True)
    description: models.TextField = models.TextField()

    def __str__(self):
        """Return the application name."""
        return self.name


class ConnectionType(models.Model):
    """Model for the connection type."""

    name: models.CharField = models.CharField(max_length=255, unique=True)
    description: models.TextField = models.TextField()
    unique_port: models.BooleanField = models.BooleanField(default=False)

    def __str__(self):
        """Return the connection type name."""
        return self.name


class Registrar(models.Model):
    """Model for the registrar."""

    name: models.CharField = models.CharField(max_length=255, unique=True)
    url: models.URLField = models.URLField()

    def __str__(self):
        """Return the registrar name."""
        return self.name


class DomainName(models.Model):
    """Model for the domain name."""

    name: models.CharField = models.CharField(max_length=255, unique=True)
    registrar: models.ForeignKey = models.ForeignKey(
        Registrar, on_delete=models.RESTRICT
    )

    def __str__(self):
        """Return the domain name."""
        return self.name


class Vendor(models.Model):
    """Model for the vendor."""

    name: models.CharField = models.CharField(max_length=255, unique=True)
    url: models.URLField = models.URLField()

    def __str__(self):
        """Return the vendor name."""
        return self.name


class Model(models.Model):
    """Model for the model."""

    name: models.CharField = models.CharField(max_length=255, unique=True)
    vendor: models.ForeignKey = models.ForeignKey(Vendor, on_delete=models.RESTRICT)

    def __str__(self):
        """Return the model name."""
        return self.name


class DeviceType(models.Model):
    """Model for the device type."""

    name: models.CharField = models.CharField(max_length=255, unique=True)
    image: models.CharField = models.CharField(max_length=20)
    description: models.TextField = models.TextField()

    def __str__(self):
        """Return the device type name."""
        return self.name


class OperatingSystem(models.Model):
    """Model for the operating system."""

    name: models.CharField = models.CharField(max_length=255, unique=True)
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
    hardware_vendor: models.ForeignKey = models.ForeignKey(
        Vendor, on_delete=models.RESTRICT
    )
    model: models.ForeignKey = models.ForeignKey(Model, on_delete=models.RESTRICT)
    device_type: models.ForeignKey = models.ForeignKey(
        DeviceType, on_delete=models.RESTRICT
    )
    applications: models.ManyToManyField = models.ManyToManyField(
        Application, null=True, blank=True
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


class Subdomain(models.Model):
    """Model for the subdomain."""

    name: models.CharField = models.CharField(max_length=255)
    domain_name: models.ForeignKey = models.ForeignKey(
        DomainName, on_delete=models.CASCADE
    )

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

    def __str__(self):
        """Return the website name."""
        return self.name
