"""Admin configuration for the Network application."""
from django.contrib import admin

from network.models import (
    AdditionalAnsibleGroup,
    AnsibleDeviceConfiguration,
    Application,
    ConnectionType,
    Device,
    DeviceType,
    DomainName,
    Model,
    OperatingSystem,
    Registrar,
    Vendor,
    Website,
)


@admin.register(AdditionalAnsibleGroup)
class AdditionalAnsibleGroupAdmin(admin.ModelAdmin):
    """Additional Ansible Group admin."""

    list_display = (
        "name",
        "description",
        "parent",
    )
    ordering = ("name",)


@admin.register(AnsibleDeviceConfiguration)
class AnsibleDeviceConfigurationAdmin(admin.ModelAdmin):
    """Additional Ansible Device Configuration admin."""

    list_display = (
        "for_device",
        "name",
    )
    ordering = ("for_device",)


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    """Configure the admin page."""

    list_display = (
        "name",
        "description",
    )
    ordering = ("name",)
    search_fields = (
        "name",
        "description",
    )


@admin.register(ConnectionType)
class ConnectionTypeAdmin(admin.ModelAdmin):
    """Configure the admin page."""

    list_display = ("name",)
    ordering = ("name",)
    search_fields = ("name",)


@admin.register(Registrar)
class RegistrarAdmin(admin.ModelAdmin):
    """Configure the admin page."""

    list_display = (
        "name",
        "url",
    )
    ordering = ("name",)
    search_fields = ("name",)


@admin.register(DomainName)
class DomainNameAdmin(admin.ModelAdmin):
    """Configure the admin page."""

    list_display = (
        "name",
        "registrar",
    )
    ordering = ("name",)
    search_fields = ("name",)


@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    """Configure the admin page."""

    list_display = (
        "name",
        "url",
    )
    ordering = ("name",)
    search_fields = ("name",)


@admin.register(Model)
class ModelAdmin(admin.ModelAdmin):
    """Configure the admin page."""

    list_display = (
        "name",
        "vendor",
    )
    ordering = ("name",)
    search_fields = ("name",)


@admin.register(DeviceType)
class DeviceTypeAdmin(admin.ModelAdmin):
    """Configure the admin page."""

    list_display = ("name",)
    ordering = ("name",)
    search_fields = ("name",)


@admin.register(OperatingSystem)
class OperatingSystemAdmin(admin.ModelAdmin):
    """Configure the admin page."""

    list_display = ("name", "vendor")
    ordering = ("name",)
    search_fields = ("name",)


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    """Configure the admin page."""

    list_display = (
        "hostname",
        "ip_address",
        "device_type",
    )
    ordering = ("hostname",)
    search_fields = ("hostname",)


@admin.register(Website)
class WebsiteAdmin(admin.ModelAdmin):
    """Configure the admin page."""

    list_display = (
        "name",
        "subdomain",
        "full_url",
    )
    ordering = ("name",)
    search_fields = ("name",)
