"""Models for the network application."""
from django.db import models


class AdditionalAnsibleGroup(models.Model):
    """Model for Ansible group."""

    name: models.CharField = models.CharField(max_length=255, unique=True)
    alias: models.CharField = models.CharField(max_length=255, blank=True)
    parent: models.ForeignKey = models.ForeignKey(
        to="self", on_delete=models.RESTRICT, null=True, blank=True
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

    def __str__(self):
        """Return the application name."""
        return self.name

    class Meta:
        """Meta class."""

        verbose_name = "Application"
        verbose_name_plural = "Applications"


class ConnectionType(models.Model):
    """Model for the connection type."""

    name: models.CharField = models.CharField(max_length=255, unique=True)
    unique_port: models.BooleanField = models.BooleanField(default=False)

    def __str__(self):
        """Return the connection type name."""
        return self.name

    class Meta:
        """Meta class."""

        verbose_name = "Connection type"
        verbose_name_plural = "Connection types"


class Registrar(models.Model):
    """Model for the registrar."""

    name: models.CharField = models.CharField(max_length=255, unique=True)
    url: models.URLField = models.URLField()

    def __str__(self):
        """Return the registrar name."""
        return self.name

    class Meta:
        """Meta class."""

        verbose_name = "Registrar"
        verbose_name_plural = "Registrars"


class DomainName(models.Model):
    """Model for the domain name."""

    name: models.CharField = models.CharField(max_length=255, unique=True)
    registrar: models.ForeignKey = models.ForeignKey(
        to=Registrar, on_delete=models.RESTRICT
    )

    def __str__(self):
        """Return the domain name."""
        return self.name

    class Meta:
        """Meta class."""

        verbose_name = "Domain name"
        verbose_name_plural = "Domain names"


class Vendor(models.Model):
    """Model for the vendor."""

    name: models.CharField = models.CharField(max_length=255, unique=True)
    url: models.URLField = models.URLField()

    def __str__(self):
        """Return the vendor name."""
        return self.name

    class Meta:
        """Meta class."""

        verbose_name = "Vendor"
        verbose_name_plural = "Vendors"


class Model(models.Model):
    """Model for the model."""

    name: models.CharField = models.CharField(max_length=255, unique=True)
    vendor: models.ForeignKey = models.ForeignKey(to=Vendor, on_delete=models.RESTRICT)

    def __str__(self):
        """Return the model name."""
        return self.name

    class Meta:
        """Meta class."""

        verbose_name = "Model"
        verbose_name_plural = "Models"


class DeviceType(models.Model):
    """Model for the device type."""

    name: models.CharField = models.CharField(max_length=255, unique=True)
    image: models.CharField = models.CharField(max_length=20)

    def __str__(self):
        """Return the device type name."""
        return self.name

    class Meta:
        """Meta class."""

        verbose_name = "Device type"
        verbose_name_plural = "Device types"


class OperatingSystem(models.Model):
    """Model for the operating system."""

    name: models.CharField = models.CharField(max_length=255, unique=True)
    alias: models.CharField = models.CharField(max_length=255, blank=True)
    vendor: models.ForeignKey = models.ForeignKey(to=Vendor, on_delete=models.RESTRICT)
    parent: models.ForeignKey = models.ForeignKey(
        to="self", on_delete=models.RESTRICT, null=True, blank=True
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

    class Meta:
        """Meta class."""

        verbose_name = "Operating system"
        verbose_name_plural = "Operating systems"


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
        to=OperatingSystem, on_delete=models.RESTRICT
    )
    additional_ansible_groups: models.ManyToManyField = models.ManyToManyField(
        to=AdditionalAnsibleGroup,
        blank=True,
    )
    hardware_vendor: models.ForeignKey = models.ForeignKey(
        to=Vendor, on_delete=models.RESTRICT
    )
    model: models.ForeignKey = models.ForeignKey(to=Model, on_delete=models.RESTRICT)
    device_type: models.ForeignKey = models.ForeignKey(
        to=DeviceType, on_delete=models.RESTRICT
    )
    applications: models.ManyToManyField = models.ManyToManyField(
        to=Application, blank=True
    )
    connected_too: models.ForeignKey = models.ForeignKey(
        to="self", on_delete=models.RESTRICT, null=True, blank=True
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


class AnsibleVariables(models.Model):
    """Model for the Ansible variable configuration."""

    name: models.CharField = models.CharField(max_length=255)

    def __str__(self):
        """Return the Ansible variable name."""
        return self.name

    class Meta:
        """Meta class."""

        verbose_name = "Ansible variable"
        verbose_name_plural = "Ansible variables"


class AnsibleDeviceConfiguration(models.Model):
    """Model for the Ansible device configuration."""

    for_device: models.ForeignKey = models.ForeignKey(
        to=Device, on_delete=models.CASCADE
    )
    name: models.ForeignKey = models.ForeignKey(
        to=AnsibleVariables, on_delete=models.CASCADE
    )
    value: models.CharField = models.CharField(max_length=255)

    def __str__(self):
        """Return the Ansible device configuration name."""
        return f"{self.for_device.hostname} - {self.name}"

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


class Website(models.Model):
    """Model for the website."""

    name: models.CharField = models.CharField(max_length=255, unique=True)
    subdomain: models.CharField = models.CharField(
        max_length=255, blank=True, null=True
    )
    domain_name: models.ForeignKey = models.ForeignKey(
        to=DomainName, on_delete=models.RESTRICT, null=True, blank=True
    )
    hosted_on: models.ForeignKey = models.ForeignKey(
        to=Device, on_delete=models.RESTRICT
    )
    secure: models.BooleanField = models.BooleanField(default=True)
    port: models.IntegerField = models.IntegerField(null=True, blank=True)
    path: models.CharField = models.CharField(max_length=255, null=True, blank=True)
    description: models.TextField = models.TextField(null=True, blank=True)

    def __str__(self):
        """Return the subdomain name."""
        return self.name

    @property
    def full_url(self):
        """Return the full url."""
        port = f":{self.port}" if self.port else ""
        path = self.path or ""
        protocol = "https" if self.secure else "http"
        return (
            f"{protocol}://{self.subdomain}.{self.domain_name.name}{port}{path}"
            if any([self.subdomain, self.domain_name])
            else f"{protocol}://{self.hosted_on.ip_address}{port}{path}"
        )

    class Meta:
        """Subdomain` model meta class."""

        unique_together = [
            (
                "name",
                "domain_name",
            ),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=("domain_name", "port", "subdomain"),
                name="website_unique_subdomain_port",
            ),
            models.UniqueConstraint(
                fields=("hosted_on", "port"), name="website_unique_port_hosted_on"
            ),
            models.CheckConstraint(
                check=(
                    models.Q(subdomain__isnull=True)
                    & models.Q(domain_name__isnull=True)
                    | models.Q(subdomain__isnull=False)
                    & models.Q(domain_name__isnull=False)
                ),
                name="website_subdomain_or_ip",
            ),
        ]
        verbose_name = "Website"
        verbose_name_plural = "Websites"
