"""Admin configuration for the Network application."""
from django.contrib import admin

from network.models import (
    Application,
    ConnectionType,
    Device,
    DeviceType,
    DomainName,
    Model,
    OperatingSystem,
    Registrar,
    Subdomain,
    Vendor,
    Website,
)


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    """Configure the admin page."""

    list_display = (
        "name",
        "description",
    )
    ordering = ("name",)


@admin.register(ConnectionType)
class ConnectionTypeAdmin(admin.ModelAdmin):
    """Configure the admin page."""

    list_display = ("name",)
    ordering = ("name",)


@admin.register(Registrar)
class RegistrarAdmin(admin.ModelAdmin):
    """Configure the admin page."""

    list_display = (
        "name",
        "url",
    )
    ordering = ("name",)


@admin.register(DomainName)
class DomainNameAdmin(admin.ModelAdmin):
    """Configure the admin page."""

    list_display = (
        "name",
        "registrar",
    )
    ordering = ("name",)


@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    """Configure the admin page."""

    list_display = (
        "name",
        "url",
    )
    ordering = ("name",)


@admin.register(Model)
class ModelAdmin(admin.ModelAdmin):
    """Configure the admin page."""

    list_display = (
        "name",
        "vendor",
    )
    ordering = ("name",)


@admin.register(DeviceType)
class DeviceTypeAdmin(admin.ModelAdmin):
    """Configure the admin page."""

    list_display = ("name",)
    ordering = ("name",)


@admin.register(OperatingSystem)
class OperatingSystemAdmin(admin.ModelAdmin):
    """Configure the admin page."""

    list_display = ("name", "vendor")
    ordering = ("name",)


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    """Configure the admin page."""

    list_display = (
        "hostname",
        "ip_address",
        "device_type",
    )
    ordering = ("hostname",)


@admin.register(Subdomain)
class SubdomainAdmin(admin.ModelAdmin):
    """Configure the admin page."""

    list_display = (
        "name",
        "domain_name",
    )
    ordering = ("name",)


@admin.register(Website)
class WebsiteAdmin(admin.ModelAdmin):
    """Configure the admin page."""

    list_display = (
        "name",
        "subdomain",
    )
    ordering = ("name",)
